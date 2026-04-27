#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: bpsk_file_transfer_loopback2_Pluto
# Author: Frank Fu, Barry Duggan
# GNU Radio version: 3.10.12.0

from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
import logging as log

def get_state_directory() -> str:
    oldpath = os.path.expanduser("~/.grc_gnuradio")
    try:
        from gnuradio.gr import paths
        newpath = paths.persistent()
        if os.path.exists(newpath):
            return newpath
        if os.path.exists(oldpath):
            log.warning(f"Found persistent state path '{newpath}', but file does not exist. " +
                     f"Old default persistent state path '{oldpath}' exists; using that. " +
                     "Please consider moving state to new location.")
            return oldpath
        # Default to the correct path if both are configured.
        # neither old, nor new path exist: create new path, return that
        os.makedirs(newpath, exist_ok=True)
        return newpath
    except (ImportError, NameError):
        log.warning("Could not retrieve GNU Radio persistent state directory from GNU Radio. " +
                 "Trying defaults.")
        xdgstate = os.getenv("XDG_STATE_HOME", os.path.expanduser("~/.local/state"))
        xdgcand = os.path.join(xdgstate, "gnuradio")
        if os.path.exists(xdgcand):
            return xdgcand
        if os.path.exists(oldpath):
            log.warning(f"Using legacy state path '{oldpath}'. Please consider moving state " +
                     f"files to '{xdgcand}'.")
            return oldpath
        # neither old, nor new path exist: create new path, return that
        os.makedirs(xdgcand, exist_ok=True)
        return xdgcand

sys.path.append(os.environ.get('GRC_HIER_PATH', get_state_directory()))

from Deinterleaver import Deinterleaver  # grc-generated hier_block
from FEC_ENCODE import FEC_ENCODE  # grc-generated hier_block
from FEC_decoder import FEC_decoder  # grc-generated hier_block
from Interleaver_simple import Interleaver_simple  # grc-generated hier_block
from PyQt5 import QtCore
from codec2488 import codec2488  # grc-generated hier_block
from gnuradio import audio
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import vocoder
from gnuradio.vocoder import codec2
import sip
import threading



class bpsk_file_transfer_loopback2_Pluto(gr.top_block, Qt.QWidget):

    def __init__(self, MTU=18, frame_size=6):
        gr.top_block.__init__(self, "bpsk_file_transfer_loopback2_Pluto", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("bpsk_file_transfer_loopback2_Pluto")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("gnuradio/flowgraphs", "bpsk_file_transfer_loopback2_Pluto")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)
        self.flowgraph_started = threading.Event()

        ##################################################
        # Parameters
        ##################################################
        self.MTU = MTU
        self.frame_size = frame_size

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 8
        self.qpsk = qpsk = digital.constellation_rect([-0.707-0.707j, 0.707-0.707j, +0.707+0.707j, -0.707+0.707j], [0, 1, 3, 2],
        4, 2, 2, 1, 1).base()
        self.excess_bw = excess_bw = 0.35
        self.tx_on = tx_on = 0
        self.rxmod = rxmod = digital.generic_mod(qpsk, True, sps, True, excess_bw, False, False)
        self.rate = rate = 2
        self.preamble_gold = preamble_gold = [0x55,0xAA]
        self.polys = polys = [109,79]
        self.k = k = 7
        self.tx_gain = tx_gain = 89
        self.sym_bw = sym_bw = 0.088
        self.samp_rate = samp_rate = 600000
        self.rx_on = rx_on = 1-tx_on
        self.preamble_size = preamble_size = 4
        self.payload_size = payload_size = 180
        self.mod_sync_word = mod_sync_word = digital.modulate_vector_bc(rxmod.to_basic_block(), preamble_gold, [1])
        self.hdr = hdr = digital.header_format_default(digital.packet_utils.default_access_code, 0)
        self.frequency = frequency = 865200000
        self.enc_cc = enc_cc = fec.cc_encoder_make((MTU*8),k, rate, polys, 0, fec.CC_TAILBITING, True)
        self.dec_cc = dec_cc = list(map( (lambda a: fec.cc_decoder.make((MTU*8),k, rate, polys, 0, (-1), fec.CC_TAILBITING, True)),range(0,1)))
        self.data = data = 0
        self.costas_bw = costas_bw = 0.06
        self.constel = constel = digital.constellation_qpsk().base()
        self.constel.set_npwr(1.0)
        self.QT_gain = QT_gain = 50
        self.FEC_frameBits = FEC_frameBits = 80

        ##################################################
        # Blocks
        ##################################################

        self._tx_on_choices = {'Pressed': 1, 'Released': 0}

        _tx_on_toggle_button = qtgui.ToggleButton(self.set_tx_on, 'tx/rx button', self._tx_on_choices, False, 'value')
        _tx_on_toggle_button.setColors("default", "default", "default", "default")
        self.tx_on = _tx_on_toggle_button

        self.top_layout.addWidget(_tx_on_toggle_button)
        self._sym_bw_range = qtgui.Range(0.02, 0.12, 0.001, 0.088, 200)
        self._sym_bw_win = qtgui.RangeWidget(self._sym_bw_range, self.set_sym_bw, "symbol loop bw", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._sym_bw_win)
        self._excess_bw_range = qtgui.Range(0.1, 0.6, 0.05, 0.35, 200)
        self._excess_bw_win = qtgui.RangeWidget(self._excess_bw_range, self.set_excess_bw, "excess bw-constelmodulator", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._excess_bw_win)
        self._costas_bw_range = qtgui.Range(0.01, 0.08, 0.01, 0.06, 200)
        self._costas_bw_win = qtgui.RangeWidget(self._costas_bw_range, self.set_costas_bw, "costas loop bw", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._costas_bw_win)
        self.vocoder_codec2_decode_ps_0 = vocoder.codec2_decode_ps(codec2.MODE_2400)
        self._tx_gain_range = qtgui.Range(0, 89, 1, 89, 200)
        self._tx_gain_win = qtgui.RangeWidget(self._tx_gain_range, self.set_tx_gain, "Tx gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._tx_gain_win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=6,
                decimation=1,
                taps=[],
                fractional_bw=0.400)
        self.qtgui_time_sink_x_0_1 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_1.set_update_time(0.10)
        self.qtgui_time_sink_x_0_1.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_1.enable_tags(False)
        self.qtgui_time_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_1.enable_autoscale(False)
        self.qtgui_time_sink_x_0_1.enable_grid(False)
        self.qtgui_time_sink_x_0_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_1.enable_control_panel(False)
        self.qtgui_time_sink_x_0_1.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_1_win = sip.wrapinstance(self.qtgui_time_sink_x_0_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_1_win)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            2048, #size
            'Synced Constellation', #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.20)
        self.qtgui_const_sink_x_0.set_y_axis((-1.5), 1.5)
        self.qtgui_const_sink_x_0.set_x_axis((-1.5), 1.5)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(True)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['Synced Only', 'Synced & Phase-Locked', '', '', '',
            '', '', '', '', '']
        widths = [1, 2, 2, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 1, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, -1, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1, 0.3, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_const_sink_x_0_win)
        self.filter_fft_rrc_filter_0 = filter.fft_filter_ccc(1, firdes.root_raised_cosine(1, samp_rate, (samp_rate/sps), excess_bw, (11*sps)), 1)
        self.digital_symbol_sync_xx_0 = digital.symbol_sync_cc(
            digital.TED_GARDNER,
            sps,
            sym_bw,
            0.707,
            0.707,
            1.5,
            1,
            constel.base(),
            digital.IR_MMSE_8TAP,
            32,
            [])
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr, 'packet_len')
        self.digital_map_bb_0 = digital.map_bb([0,1,3,2])
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(4, digital.DIFF_DIFFERENTIAL)
        self.digital_crc32_bb_1 = digital.crc32_bb(True, 'packet', True)
        self.digital_crc32_bb_0 = digital.crc32_bb(False, "packet_len", True)
        self.digital_costas_loop_cc_0 = digital.costas_loop_cc(costas_bw, 4, False)
        self.digital_correlate_access_code_xx_ts_0 = digital.correlate_access_code_bb_ts(digital.packet_utils.default_access_code,
          2, 'packet_len')
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.digital_constellation_decoder_cb_1 = digital.constellation_decoder_cb(qpsk)
        self.digital_additive_scrambler_xx_0_0 = digital.additive_scrambler_bb(0x8A, 0x7F, 7, count=0, bits_per_byte=1, reset_tag_key="")
        self.digital_additive_scrambler_xx_0 = digital.additive_scrambler_bb(0x8A, 0x7F, 7, count=0, bits_per_byte=1, reset_tag_key="")
        self._data_tool_bar = Qt.QToolBar(self)

        if None:
            self._data_formatter = None
        else:
            self._data_formatter = lambda x: str(x)

        self._data_tool_bar.addWidget(Qt.QLabel("data"))
        self._data_label = Qt.QLabel(str(self._data_formatter(self.data)))
        self._data_tool_bar.addWidget(self._data_label)
        self.top_layout.addWidget(self._data_tool_bar)
        self.codec2488_0 = codec2488(
            Decimate=6,
            Interpolate=1,
            packet_len=6,
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_b(preamble_gold, True, 1, [])
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(2)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'packet_len', 0)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_char*1, 48)
        self.blocks_stream_to_tagged_stream_0_0_0_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, preamble_size, "packet_len")
        self.blocks_short_to_float_0 = blocks.short_to_float(1, 8192)
        self.blocks_repack_bits_bb_1_0 = blocks.repack_bits_bb(8, 1, 'packet', False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_1 = blocks.repack_bits_bb(1, 8, 'packet', False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(1, 8, "packet_len", False, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(8, 1, "packet_len", False, gr.GR_LSB_FIRST)
        self.blocks_multiply_const_vxx_2 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_cc(tx_on)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.5)
        self.audio_source_0 = audio.source(48000, '', True)
        self.audio_sink_0 = audio.sink(48000, '', True)
        self._QT_gain_range = qtgui.Range(0, 73, 1, 50, 200)
        self._QT_gain_win = qtgui.RangeWidget(self._QT_gain_range, self.set_QT_gain, "RX_gain", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._QT_gain_win)
        self.Interleaver_simple_0 = Interleaver_simple(
            Columns=8,
            Rows=20,
        )
        self.FEC_decoder_0 = FEC_decoder(
            MTU=MTU,
            cc_decoder_def=dec_cc,
        )
        self.FEC_ENCODE_0 = FEC_ENCODE(
            Frame_bits=frame_size,
            MTU=MTU,
            cc_encoder_def=enc_cc,
            packet_len="packet_len",
        )
        self.Deinterleaver_0 = Deinterleaver(
            Columns=8,
            Rows=20,
        )


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Deinterleaver_0, 0), (self.FEC_decoder_0, 0))
        self.connect((self.FEC_ENCODE_0, 0), (self.Interleaver_simple_0, 0))
        self.connect((self.FEC_ENCODE_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.FEC_decoder_0, 0), (self.blocks_repack_bits_bb_1, 0))
        self.connect((self.Interleaver_simple_0, 0), (self.blocks_tagged_stream_mux_0, 2))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_2, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.filter_fft_rrc_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_2, 0), (self.codec2488_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.digital_additive_scrambler_xx_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_crc32_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_1, 0), (self.digital_crc32_bb_1, 0))
        self.connect((self.blocks_repack_bits_bb_1_0, 0), (self.digital_additive_scrambler_xx_0_0, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.qtgui_time_sink_x_0_1, 0))
        self.connect((self.blocks_short_to_float_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.vocoder_codec2_decode_ps_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.digital_correlate_access_code_xx_ts_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0_0_0_0, 0))
        self.connect((self.codec2488_0, 0), (self.blocks_repack_bits_bb_0, 0))
        self.connect((self.digital_additive_scrambler_xx_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_additive_scrambler_xx_0_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.digital_constellation_decoder_cb_1, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_correlate_access_code_xx_ts_0, 0), (self.Deinterleaver_0, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.digital_constellation_decoder_cb_1, 0))
        self.connect((self.digital_costas_loop_cc_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.digital_crc32_bb_0, 0), (self.FEC_ENCODE_0, 0))
        self.connect((self.digital_crc32_bb_1, 0), (self.blocks_repack_bits_bb_1_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.digital_map_bb_0, 0))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.digital_costas_loop_cc_0, 0))
        self.connect((self.digital_symbol_sync_xx_0, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.filter_fft_rrc_filter_0, 0), (self.digital_symbol_sync_xx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.vocoder_codec2_decode_ps_0, 0), (self.blocks_short_to_float_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("gnuradio/flowgraphs", "bpsk_file_transfer_loopback2_Pluto")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_MTU(self):
        return self.MTU

    def set_MTU(self, MTU):
        self.MTU = MTU
        self.FEC_ENCODE_0.set_MTU(self.MTU)
        self.FEC_decoder_0.set_MTU(self.MTU)

    def get_frame_size(self):
        return self.frame_size

    def set_frame_size(self, frame_size):
        self.frame_size = frame_size
        self.FEC_ENCODE_0.set_Frame_bits(self.frame_size)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rxmod(digital.generic_mod(self.qpsk, True, self.sps, True, self.excess_bw, False, False))
        self.digital_symbol_sync_xx_0.set_sps(self.sps)
        self.filter_fft_rrc_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (11*self.sps)))

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk
        self.set_rxmod(digital.generic_mod(self.qpsk, True, self.sps, True, self.excess_bw, False, False))
        self.digital_constellation_decoder_cb_1.set_constellation(self.qpsk)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw
        self.set_rxmod(digital.generic_mod(self.qpsk, True, self.sps, True, self.excess_bw, False, False))
        self.filter_fft_rrc_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (11*self.sps)))

    def get_tx_on(self):
        return self.tx_on

    def set_tx_on(self, tx_on):
        self.tx_on = tx_on
        self.set_rx_on(1-self.tx_on)
        self.blocks_multiply_const_vxx_1_0_0.set_k(self.tx_on)

    def get_rxmod(self):
        return self.rxmod

    def set_rxmod(self, rxmod):
        self.rxmod = rxmod

    def get_rate(self):
        return self.rate

    def set_rate(self, rate):
        self.rate = rate

    def get_preamble_gold(self):
        return self.preamble_gold

    def set_preamble_gold(self, preamble_gold):
        self.preamble_gold = preamble_gold
        self.blocks_vector_source_x_0.set_data(self.preamble_gold, [])

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain

    def get_sym_bw(self):
        return self.sym_bw

    def set_sym_bw(self, sym_bw):
        self.sym_bw = sym_bw
        self.digital_symbol_sync_xx_0.set_loop_bandwidth(self.sym_bw)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.filter_fft_rrc_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/self.sps), self.excess_bw, (11*self.sps)))
        self.qtgui_time_sink_x_0_1.set_samp_rate(self.samp_rate)

    def get_rx_on(self):
        return self.rx_on

    def set_rx_on(self, rx_on):
        self.rx_on = rx_on

    def get_preamble_size(self):
        return self.preamble_size

    def set_preamble_size(self, preamble_size):
        self.preamble_size = preamble_size
        self.blocks_stream_to_tagged_stream_0_0_0_0.set_packet_len(self.preamble_size)
        self.blocks_stream_to_tagged_stream_0_0_0_0.set_packet_len_pmt(self.preamble_size)

    def get_payload_size(self):
        return self.payload_size

    def set_payload_size(self, payload_size):
        self.payload_size = payload_size

    def get_mod_sync_word(self):
        return self.mod_sync_word

    def set_mod_sync_word(self, mod_sync_word):
        self.mod_sync_word = mod_sync_word

    def get_hdr(self):
        return self.hdr

    def set_hdr(self, hdr):
        self.hdr = hdr
        self.digital_protocol_formatter_bb_0.set_header_format(self.hdr)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency

    def get_enc_cc(self):
        return self.enc_cc

    def set_enc_cc(self, enc_cc):
        self.enc_cc = enc_cc
        self.FEC_ENCODE_0.set_cc_encoder_def(self.enc_cc)

    def get_dec_cc(self):
        return self.dec_cc

    def set_dec_cc(self, dec_cc):
        self.dec_cc = dec_cc
        self.FEC_decoder_0.set_cc_decoder_def(self.dec_cc)

    def get_data(self):
        return self.data

    def set_data(self, data):
        self.data = data
        Qt.QMetaObject.invokeMethod(self._data_label, "setText", Qt.Q_ARG("QString", str(self._data_formatter(self.data))))

    def get_costas_bw(self):
        return self.costas_bw

    def set_costas_bw(self, costas_bw):
        self.costas_bw = costas_bw
        self.digital_costas_loop_cc_0.set_loop_bandwidth(self.costas_bw)

    def get_constel(self):
        return self.constel

    def set_constel(self, constel):
        self.constel = constel

    def get_QT_gain(self):
        return self.QT_gain

    def set_QT_gain(self, QT_gain):
        self.QT_gain = QT_gain

    def get_FEC_frameBits(self):
        return self.FEC_frameBits

    def set_FEC_frameBits(self, FEC_frameBits):
        self.FEC_frameBits = FEC_frameBits



def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "--MTU", dest="MTU", type=intx, default=18,
        help="Set MTU [default=%(default)r]")
    parser.add_argument(
        "--frame-size", dest="frame_size", type=intx, default=6,
        help="Set Frame Size [default=%(default)r]")
    return parser


def main(top_block_cls=bpsk_file_transfer_loopback2_Pluto, options=None):
    if options is None:
        options = argument_parser().parse_args()

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(MTU=options.MTU, frame_size=options.frame_size)

    tb.start()
    tb.flowgraph_started.set()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
