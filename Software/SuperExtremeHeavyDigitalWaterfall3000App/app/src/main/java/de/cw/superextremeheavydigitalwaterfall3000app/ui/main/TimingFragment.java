package de.cw.superextremeheavydigitalwaterfall3000app.ui.main;

import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.SeekBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import org.json.JSONException;
import org.json.JSONObject;

import de.cw.superextremeheavydigitalwaterfall3000app.R;

public class TimingFragment extends Fragment {

    private static final String ARG_SECTION_NUMBER = "timing";

    private PageViewModel pageViewModel;

    public static TimingFragment newInstance(int index) {
        TimingFragment fragment = new TimingFragment();
        Bundle bundle = new Bundle();
        bundle.putInt(ARG_SECTION_NUMBER, index);
        fragment.setArguments(bundle);
        return fragment;
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        pageViewModel = ViewModelProviders.of(this).get(PageViewModel.class);
        int index = 1;
        if (getArguments() != null) {
            index = getArguments().getInt(ARG_SECTION_NUMBER);
        }
        pageViewModel.setIndex(index);
    }

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        View timing_frame = inflater.inflate(R.layout.timing_frame, container, false);

        init((SeekBar) timing_frame.findViewById(R.id.seekBarOnTime), (TextView) timing_frame.findViewById(R.id.textViewOnTime), getResources().getString(R.string.on_time));
        init((SeekBar) timing_frame.findViewById(R.id.seekBarOffTime), (TextView) timing_frame.findViewById(R.id.textViewOffTime), getResources().getString(R.string.off_time));

        return timing_frame;
    }

    private double getValue(SeekBar seekBar) {
        return (double) seekBar.getProgress() / 100 * 0.005;
    }

    private String getResponse(final View root) throws JSONException {
        JSONObject request = new JSONObject();
        SeekBar seekBarOnTime = root.findViewById(R.id.seekBarOnTime);
        SeekBar seekBarOffTime = root.findViewById(R.id.seekBarOffTime);


        double percentOffTime = (double) seekBarOffTime.getProgress() / 100;

        request.put("on_time", getValue(seekBarOnTime));
        request.put("off_time", getValue(seekBarOffTime));

        return request.toString();
    }

    private void init(SeekBar seekBar, final TextView textView, final String label) {
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {

            @SuppressLint({"SetTextI18n", "ShowToast"})
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                textView.setText(label + " " + getValue(seekBar));
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });
    }
}