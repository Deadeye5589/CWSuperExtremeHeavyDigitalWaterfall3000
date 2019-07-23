package de.cw.superextremeheavydigitalwaterfall3000app.ui.main;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.lifecycle.ViewModelProviders;

import de.cw.superextremeheavydigitalwaterfall3000app.R;

public class EffectFragment extends Fragment {

    private static final String ARG_SECTION_NUMBER = "effect";

    private PageViewModel pageViewModel;

    public static EffectFragment newInstance(int index) {
        EffectFragment fragment = new EffectFragment();
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
        View effect_frame = inflater.inflate(R.layout.effect_frame, container, false);
        return effect_frame;
    }
}
