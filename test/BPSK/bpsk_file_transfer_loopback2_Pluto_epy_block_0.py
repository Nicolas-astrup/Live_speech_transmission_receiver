import numpy as np
import pmt
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, packet_len=160, cols=16):
        gr.sync_block.__init__(
            self,
            name='Deinterleaver',
            in_sig=[np.uint8],
            out_sig=[np.uint8]
        )
        self.packet_len = packet_len
        self.cols = cols
        self.rows = packet_len // cols
        self.buffer = []
        self.copying = False
        self.remaining = 0
        self.set_tag_propagation_policy(gr.TPP_DONT)

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        n_produced = 0

        tags = self.get_tags_in_window(0, 0, len(in0))
        for tag in tags:
            if pmt.to_python(tag.key) == 'packet_len':
                self.copying = True
                self.remaining = pmt.to_python(tag.value)
                self.buffer = []

        for i, byte in enumerate(in0):
            if self.copying and self.remaining > 0:
                self.buffer.append(byte)
                self.remaining -= 1

                if self.remaining == 0:
                    packet = np.array(self.buffer, dtype=np.uint8)
                    matrix = packet.reshape(self.cols, self.rows)
                    deinterleaved = matrix.T.flatten()

                    out[n_produced:n_produced + self.packet_len] = deinterleaved

                    self.add_item_tag(
                        0,
                        self.nitems_written(0) + n_produced,
                        pmt.intern('packet_len'),
                        pmt.from_long(self.packet_len)
                    )

                    n_produced += self.packet_len
                    self.copying = False
                    self.buffer = []

        return n_produced