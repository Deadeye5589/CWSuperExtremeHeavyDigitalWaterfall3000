/*
 * WasserfallTreiber.c
 *
 * Created: 18.07.2019 - 12:00
 * Author : Ich
 */ 


// Defines -----------------------------------------------------------------
#define BUFFER_SIZE				4096	//Size of the UART Rx ring buffer
#define DRV8860DELAY			4		//Delay in us for DRV8860 drivers
#define F_CPU 32000000UL				//CPU frequency generated by internal clock
#define EEPROM_BYTE_ADDR_1		0		//Location within page to store high byte no of used relays
#define EEPROM_BYTE_ADDR_2		0		//Location within page to store low byte no of used relays
#define EEPROM_PAGE_ADDR		0		//EEPROM page address to store no of used relays

// Include headers ---------------------------------------------------------
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include "ringbuffer.h"
#include "eeprom_driver.h"

// Global variables ---------------------------------------------------------
volatile uint16_t state_count = 0;		//Status Counter for the frame state machine
volatile uint16_t frame_length = 0;		//Number of bits a single frame will address
volatile uint8_t data = 0;				//Data from the UART Rx
volatile uint8_t byte_ready = 0;		//Indicate to main loop that an unprocessed frame came in via UART
uint8_t USART_Data[BUFFER_SIZE];		//UART Rx ring buffer
RingBuffer_t Buffer;					//Construction of ringer buffer struct

volatile uint16_t config = 1;			//No of used relays 
volatile uint8_t store_eeprom = 0;		//Indicated to main loop that we want to store value into EEPROM

// Enumerations -------------------------------------------------------------
enum {start, framelength_1, framelength_2, payload, setup_1, setup_2};		//Status of state machine to be stored in state_count


// definition of functions ---------------------------------------------------------
// function name: init_ports()
// configuration of port pins
void init_ports(void){
	PORTC.DIRSET = (1<<PORT7) | (1<<PORT3) | (1<<PORT0);				//Set PC7, PC3 and PC0 as output
	PORTCFG.CLKEVOUT = PORTCFG_CLKOUT_PC7_gc;							//Route clock to PC7 output
	PORTD.DIRSET = (1<<PORT6) | (1<<PORT4) | (1<<PORT3) | (1<<PORT1);	//Out for DRV8860 Enable, Data Out, Clock and Latch
	PORTD.DIRSET = (1<<PORT7) | (1<<PORT6) | (1<<PORT5) | (1<<PORT4);	//Hardware SPI alternative for DRV8860 control 
}


// function name: init_clocks()
// Activates the external 16 MHz crystal
// Uses internal PLL to generate 32 MHz main clock frequency
void init_clocks(void){
	OSC.CTRL |= OSC_RC32MEN_bm | OSC_RC32KEN_bm;  // Enable the internal 32MHz & 32KHz oscillators
	while(!(OSC.STATUS & OSC_RC32KRDY_bm));       // Wait for 32Khz oscillator to stabilize
	while(!(OSC.STATUS & OSC_RC32MRDY_bm));       // Wait for 32MHz oscillator to stabilize
	DFLLRC32M.CTRL = DFLL_ENABLE_bm ;             // Enable DFLL - defaults to calibrate against internal 32Khz clock
	CCP = CCP_IOREG_gc;                           // Disable register security for clock update
	CLK.CTRL = CLK_SCLKSEL_RC32M_gc;              // Switch to 32MHz clock
	OSC.CTRL &= ~OSC_RC2MEN_bm;                   // Disable default 2Mhz oscillator
}


// function name: init_uart()
// Configure UART to 115200 Baud 8N1 format
// Use Rx and Tx, Rx interrupt based
// with CLK2X = 0, BSCALE = -6 error <0,01%, BSEL = 1047
void init_uart(void){
	USARTC0.BAUDCTRLA = 0x417 & 0x0FF;											//Write lower 8 bits of BSEL to RegA
	USARTC0.BAUDCTRLB = ((0x417 & 0xF00) >> 0x08);								//Write higher 4 bits of BSEL to RegB
	USARTC0.BAUDCTRLB |= ((-6 & 0x0F) << 0x04);									//Write BSCALE to bit 4...7 of RegB 
	USARTC0.CTRLA = USART_RXCINTLVL_LO_gc;										//Enable receive interrupt with low priority
	USARTC0.STATUS |= USART_RXCIF_bm;											//Clear interrupt flag to have clean start condition
	USARTC0.CTRLB = USART_TXEN_bm | USART_RXEN_bm;								//Enable Tx and Rx for UART on PortC
	USARTC0.CTRLC = USART_CHSIZE_8BIT_gc;										//Define data byte to be 8 bits
	USARTC0.CTRLC &= ~(USART_PMODE0_bm | USART_PMODE1_bm | USART_SBMODE_bm);	//Set to 8N1 Mode
}


// function name: init_spi_uart()
// Configure UART be used as SPI interface
// Use Tx only with 250 kBit / s
void init_spi_uart(void){
	USARTD0.CTRLB = USART_TXEN_bm;			//Enable transmitter of UART at Port D
	USARTD0.CTRLC = USART_CMODE_MSPI_gc;	//SPI mode 0 CPOL and CPHA at 0
	USARTD0.BAUDCTRLA = 0x3F;				//BSEL = 63 for 250 kBit / s 
}


// function name: init_timer()
// Configure timer 0 (TCC0) 
// 36 ms interrupt interval
// Based on Baud rate of 115200 and maximum number of relays 4096
// t_max = 1/ 115200 baud * 4096
// t_max = 35,55 ms rounded to 36ms which is 27.77 Hz  
void init_timer(void){
	TCC0.CTRLB = TC_WGMODE_NORMAL_gc;			//Set timer to normal mode, frequency generation via PER register
	TCC0.CTRLA = TC_CLKSEL_OFF_gc;				//Timer is disabled after init
	//TCC0.CTRLA = TC_CLKSEL_DIV64_gc;			//Prescaler to 64, also used to (re)enable timer 
	TCC0.PER = 18000;							//Per register setting so timer frequency equals 27.77 Hz (fout = f_Cpu / (Prescaler*(PER+1))	
	TCC0.INTCTRLA = TC_OVFINTLVL_LO_gc;			//Enable timer overflow interrupt		
}


// function name: DRV8860_send_data()
// send out 8 bits of data to DRV8860 driver
// Software driver for bit banging
// Not necessary for Gehirn V1.0 PCB
void DRV8860_send_data(uint8_t drv8860_data){
	uint8_t i = 0;
	PORTD.OUTCLR = PIN1_bm;  //Clock Low
	for (i=8; i!=0; i--)	 //Send out byte
	{
		/*
		set data out port accordingly to current bit status to either high or low
		*/
		if (drv8860_data&0x80)
		{
			PORTD.OUTSET = PIN2_bm;
		} 
		else
		{
			PORTD.OUTCLR = PIN2_bm;
		}
		_delay_us(DRV8860DELAY);				//Delay 4us
		PORTD.OUTSET = PIN1_bm;					//Clock High
		drv8860_data = (drv8860_data<<1);		//Shift to next bit position of byte
		_delay_us(DRV8860DELAY);				//Delay 4us
		/* 
		left CLK HIGH at after the last data transfered
		avoid unwanted fault register pushed out.
		*/
		if (i > 1)
		{
			PORTD.OUTCLR = PIN1_bm;				//Clock Low
		}	
	}
}


// function name: DRV8860_cleanup()
// Clean registers of DRV8860 to avoid unwanted fault register pushed out
// Call with number of drivers that are used for the waterfall
// Each driver has 8 channels that will be cleared during startup
void DRV8860_cleanup(uint16_t no_of_drivers){
	//set all outputs to low
	PORTD.OUTSET = PIN4_bm;									//Latch High
	_delay_us(DRV8860DELAY);								//Delay 4us
	PORTD.OUTCLR = PIN0_bm;									//Latch Low
	for(uint16_t i = 0; i < 8 * no_of_drivers; i++)
	{
		while(!(USARTD0.STATUS & USART_DREIF_bm));			//Wait for transmission buffer to be empty
			USARTD0.DATA = 0;								//Send data to first DRV8860 driver
	}
	_delay_us(DRV8860DELAY);								//Delay 4us
	PORTD.OUTSET = PIN4_bm;									//Latch High
}


// function name: send message()
// Send a message through the UART
// Add CR + LF at the end of the message 
void send_message(char* message){
	while(*message)										//As long as the message is
	{
		while(!(USARTC0.STATUS & USART_DREIF_bm));		//Check that UART transmission buffer is empty
		USARTC0.DATA = *message++;						//Send a byte of the message
	}
	while(!(USARTC0.STATUS & USART_DREIF_bm));			//CR + LF
	USARTC0.DATA = 0x0D;
	while(!(USARTC0.STATUS & USART_DREIF_bm));
	USARTC0.DATA = 0x0A;
}


// function name: save_eeprom()
// Stores relay config into EEPROM
// Converts 16 bit config variable into two 8 bit values 
// Gives UART message when completed
void save_eeprom(uint16_t config_value){
	EEPROM_FlushBuffer();							//Flush buffer just to be sure when we start
	EEPROM_DisableMapping();
	EEPROM_WriteByte(EEPROM_PAGE_ADDR, EEPROM_BYTE_ADDR_2, (config_value & 0xFF));	//Store low byte to EEPROM
	EEPROM_WriteByte(EEPROM_PAGE_ADDR, EEPROM_BYTE_ADDR_1, (config_value >> 8));	//Store high byte to EEPROM

	char* report = "Config saved";					//The  message you get
	send_message(report);							//Send message via UART
	store_eeprom = 0;								//EEPRPOM value was saved
}


// function name: start_timer()
// Calculates the timer length based on the value of bytes per frame
// Sets timer PER register accordingly 
// Starts Timer 0 that we use like a watchdog in case the frame message is not completed in time
void start_timer(uint16_t duration){
	float ftimer = 0;				//Frequency of the timer interval
	uint8_t pre = 64;				//Same prescaler value as set during timer_init()
	uint32_t baud = 115200;			//Same as UART baud rate set in uart_init()
	float symbol = 0;				//Symbol duration based on 1 / baud	* no of bytes per frame

	symbol = (1 / baud) * duration;			//Calculate how long the whole frame will take
	ftimer = (F_CPU - 1) / (symbol * pre);	//Calculate the new setting of the periode register of Timer0
	TCC0.PER = (uint16_t)ftimer;			//Set the new timer periode
	TCC0.CTRLA = TC_CLKSEL_DIV64_gc;		//And start the timer by setting the prescaler 
}


// function name: stop_timer()
// Stops Timer0 by setting the prescaler to Off and resets counter register 
void stop_timer(void){
	TCC0.CTRLA = TC_CLKSEL_OFF_gc;							//Stop Timer0 since frame was received completely
	TCC0.CNT = 0x0000;										//Reset timer counter register to 0
}


// interrupt handlers ---------------------------------------------------------
// function name: UARTC0_Rx_Interrupt
// UART Receive interrupt to write received data into ring buffer 
// but also handels the state machines for Frame reception or system config
ISR(USARTC0_RXC_vect)
{
 	data = USARTC0.DATA;										//Receive 1 byte from UART
	USARTC0.DATA = data;										//Send out same byte as mirror per UART
	if(data == 0x53 && state_count == start){					//Check if byte "S" indicates start of new frame and state machine is at start
		state_count = framelength_1;							//A new frame was started, now we need to read in the next 2 bytes to determine the frame length
	}
	else if (state_count == framelength_1)						//Copy second byte of a new frame into the frame length value
	{
		frame_length = (data << 8);								//The second byte needs to be the high byte of the 16 bit frame length value
		state_count = framelength_2;
	}
	else if (state_count == framelength_2)						//Copy third byte of a new frame into the frame length value
	{
		frame_length = frame_length | data;						//The third byte needs to be the low byte of the 16 bit frame length value
		if(frame_length == 0 || frame_length > 4069){			//Sanity check for frame size
			char* report = "Frame length error";					//The error message you get
			send_message(report);								//Send the message via UART
			state_count = start;								//Go back to start don't take 4000�
		}
		start_timer(frame_length);								//Start our "watchdog" like timer
		state_count = payload;									
	}
	else if (state_count == payload && frame_length > 0)		//All other bytes are payload of a frame
	{
		RingBuffer_Save(&Buffer, data);							//Store byte into ring buffer
		frame_length--;											//We do not want to receive more frames than specified
	}
	else if (state_count == payload && frame_length == 0) {
		RingBuffer_Save(&Buffer, data);							//Store last byte into ring buffer
		byte_ready = 1;											//Main loop may process the received frame
	}
	
	else if (data == 0x43 && state_count == start){				//Check if byte "C" indicates setup routine and state machine is at start
		state_count = setup_1;
	}
	else if (state_count == setup_1){							//Read next 2 bytes to get number of drivers max 512
		config = (data << 8);
		state_count = setup_2;
	}
	else if (state_count == setup_1){							//Read next 2 bytes to get number of drivers max 512
		config = config | data;
		if(config == 0 || frame_length > 512){					//Sanity check for number of relays
			char* report = "Config error";						//The error message you get
			send_message(report);								//Send the message via UART
			state_count = start;								//Go back to start don't take 4000�
		}
		else{
			store_eeprom = 1;
		}
		state_count = setup_2;
	}
	
}


// function name: TCC0_OVF_vect
// Timer0 (TCC0) overflow interrupt
// Used to reset state machine and ring buffer, 
// if frame is not completed within expected time
ISR(TCC0_OVF_vect)
{
	stop_timer();								//The timeout was trigged so we can stop the timer for now
	RingBuffer_Cleanup(&Buffer, USART_Data);	//Clear the ring buffer 
	char* timeout = "Frame time out";			//Send message via UART that frame was timed out
	send_message(timeout);
	state_count = start;						//Reset the state machine
}


// main program starts here ---------------------------------------------------------
int main(void)
{
	init_clocks();
	init_ports();
	init_uart();
	init_timer();

	config = EEPROM_ReadByte(EEPROM_PAGE_ADDR, EEPROM_BYTE_ADDR_1)<<8; 	//Read number of used relays that was stored in EEPROM
	config |= EEPROM_ReadByte(EEPROM_PAGE_ADDR, EEPROM_BYTE_ADDR_2); 	//First high than low byte
	
	DRV8860_cleanup(config);								//Initialize DRV8860 drivers 
	
	RingBuffer_Init(&Buffer, USART_Data, BUFFER_SIZE);		//Initialize the ring buffer
	state_count = start;									//Set state machine to start
	
	PMIC.CTRL = PMIC_LOLVLEN_bm;							//Enable low level interrupts
	sei();													//Global enable of interrupts

	PORTD.OUTSET = PIN6_bm;									//Enable the DRV8860 output stages
	
	char* Data = "CWSuperExtremeHeavyDigitalWaterfall3000";	//The formal greeting
	send_message(Data);										//Send the message via UART


	
    /* Replace with your application code */
    while (1) 
    {
		if(byte_ready){

			stop_timer();											//Frames was completely received so we can stop the timeout

			//Output content of ring buffer on DRV8860 drivers 
			PORTD.OUTSET = PIN4_bm;									//Latch High
			_delay_us(DRV8860DELAY);								//Delay 4us
			PORTD.OUTCLR = PIN4_bm;									//Latch Low
			while(!RingBuffer_IsEmpty(&Buffer))						//Keep sending data until buffer becomes empty
			{
				while(!(USARTD0.STATUS & USART_DREIF_bm));			//Wait for SPI transmission buffer to be empty
				USARTD0.DATA = RingBuffer_Load(&Buffer);			//Send data to first DRV8860 driver
			}
			_delay_us(DRV8860DELAY);								//Delay 4us
			PORTD.OUTSET = PIN4_bm;									//Latch High
			
			char* completed = "F";
			send_message(completed);								//Send letter F to indicate Gehirn that frame was drawn on water curtain
			
			byte_ready = 0;											//The whole frame buffer was processed
			state_count = start;									//All data was displayed on the waterfall and we are ready to receive a new frame
		}

		if(store_eeprom){
			save_eeprom(config);									//Save config to EEPROM
		}

		_delay_ms(500);												//basically nop, nop, nop
		PORTC.OUTSET = PIN0_bm;										//Set PC0 to high (LED on)
		_delay_ms(500);												//more of the nop, nop, nop
		PORTC.OUTCLR = PIN0_bm;										//Clear PC0 to low (LED off)
    }
}

