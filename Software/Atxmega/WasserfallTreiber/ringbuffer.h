/*
 * RingBuffer.h
 *
 *  Copyright (C) Daniel Kampert, 2018
 *	Website: www.kampis-elektroecke.de
 *  File info: Generic ring buffer
  GNU GENERAL PUBLIC LICENSE:
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.
  You should have received a copy of the GNU General Public License
  along with this program. If not, see <http://www.gnu.org/licenses/>.
  Errors and omissions should be reported to DanielKampert@kampis-elektroecke.de
 */ 

#ifndef RINGBUFFER_H_
#define RINGBUFFER_H_

 #include <avr/io.h>
 
 typedef struct 
 {
	 /*
		Pointer to data current storage location
	 */
	 uint8_t* InPtr;
	 
	 /*
		Pointer to data current retrieval location
	 */
	 uint8_t* OutPtr;
	 
	 /*
		 Pointer to the start position of the ring buffer
	 */	 
	 uint8_t* RingStart;
	 
	 /*
		 Pointer to the end position of the ring buffer
	 */
	 uint8_t* RingEnd;
	 
	 /*
		 Size of the ring buffer
	 */
	 uint16_t Size;
	 
	 /*
		Bytes stored in the ring buffer
	 */
	 uint16_t ByteCount;
 } RingBuffer_t;

 /*****************************************************************************
  * @brief               Initialize a new ring buffer.
  *
  * @param Buffer		 Pointer to ring buffer object
  * @param Data			 Pointer to data array
  * @param Size			 Size of the data array
 *******************************************************************************/
 static inline void RingBuffer_Init(RingBuffer_t* Buffer, uint8_t* Data, const uint16_t Size) __attribute__ ((always_inline)); 
 static inline void RingBuffer_Init(RingBuffer_t* Buffer, uint8_t* Data, const uint16_t Size)
 {
	 Buffer->InPtr = Data;
	 Buffer->OutPtr = Data;
	 Buffer->RingStart = &Data[0];
	 Buffer->RingEnd = &Data[Size];
	 Buffer->Size = Size;
	 Buffer->ByteCount = 0;
 }

 /*****************************************************************************
  * @brief               Save a new data byte at the current position.
  *
  * @param Buffer		 Pointer to ring buffer object
  * @param Data			 Data byte
 *******************************************************************************/
 static inline void RingBuffer_Save(RingBuffer_t* Buffer, const uint8_t Data) __attribute__ ((always_inline)); 
 static inline void RingBuffer_Save(RingBuffer_t* Buffer, const uint8_t Data)
 {
	 *Buffer->InPtr = Data;

	 if(++Buffer->InPtr == Buffer->RingEnd)
	 {
		 Buffer->InPtr = Buffer->RingStart;
	 }

	 Buffer->ByteCount++;
 }

 /*****************************************************************************
  * @brief               Load the current data byte from the buffer
  *
  * @param Buffer		 Pointer to ring buffer object
  *
  * @return				 Data byte
 *******************************************************************************/
 static inline uint8_t RingBuffer_Load(RingBuffer_t* Buffer) __attribute__ ((always_inline)); 
 static inline uint8_t RingBuffer_Load(RingBuffer_t* Buffer)
 {
	 uint8_t Data = *Buffer->OutPtr;
	 
	 if(++Buffer->OutPtr == Buffer->RingEnd)
	 {
		 Buffer->OutPtr = Buffer->RingStart;
	 }

	 Buffer->ByteCount--;

	 return Data; 
 }
 
 /*****************************************************************************
  * @brief               Check if the buffer is empty.
  *
  * @param Buffer		 Pointer to ring buffer object
  *
  * @return				 1 if the buffer is empty
 *******************************************************************************/
 static inline uint8_t RingBuffer_IsEmpty(const RingBuffer_t* Buffer) __attribute__ ((always_inline));
 static inline uint8_t RingBuffer_IsEmpty(const RingBuffer_t* Buffer)
 {
	 return (Buffer->ByteCount == 0);
 }

 /*****************************************************************************
  * @brief               Check if the buffer is full.
  *
  * @param Buffer		 Pointer to ring buffer object
  *
  * @return				 1 if the buffer is full
 *******************************************************************************/
 static inline uint8_t RingBuffer_IsFull(const RingBuffer_t* Buffer) __attribute__ ((always_inline));
 static inline uint8_t RingBuffer_IsFull(const RingBuffer_t* Buffer)
 {
	 return (Buffer->ByteCount == Buffer->Size);
 }

 /*****************************************************************************
  * @brief               Get the byte count in the buffer
  *
  * @param Buffer		 Pointer to ring buffer object
  *
  * @return				 Bytes in the buffer
 *******************************************************************************/
 static inline uint16_t RingBuffer_GetBytes(const RingBuffer_t* Buffer) __attribute__ ((always_inline));
 static inline uint16_t RingBuffer_GetBytes(const RingBuffer_t* Buffer)
 {
	 return Buffer->ByteCount;
 }
 
  /*****************************************************************************
  * @brief               Cleanup the ring buffer
  *
  * @param Buffer		 Pointer to ring buffer object
  * 
  *
 *******************************************************************************/
 static inline void RingBuffer_Cleanup(RingBuffer_t* Buffer, uint8_t* Data) __attribute__ ((always_inline)); 
 static inline void RingBuffer_Cleanup(RingBuffer_t* Buffer, uint8_t* Data)
 {
	 Buffer->InPtr = Data;
	 Buffer->OutPtr = Data;
	 Buffer->ByteCount = 0;
 }

#endif /* RINGBUFFER_H_ */