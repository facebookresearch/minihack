from minihack.tiles import glyph2tile, MAXOTHTILE
import numpy as np
import pkg_resources
import pickle
import os


class GlyphMapper:
    """This class is used to map glyphs to rgb pixels."""

    def __init__(self):
        self.tiles = self.load_tiles()

    def load_tiles(self):
        """This function expects that tile.npy already exists.
        If it doesn't, call make_tiles.py in win/
        """

        tile_rgb_path = os.path.join(
            pkg_resources.resource_filename("nle", "tiles"),
            "tiles.pkl",
        )

        return pickle.load(open(tile_rgb_path, "rb"))

    def glyph_id_to_rgb(self, glyph_id):
        # TODO fix glyph=0 (invisible parts: now showing monster:0 icon)
        # Looks up pre-processed rgb for the tile and returns it
        tile_id = glyph2tile[glyph_id]
        assert 0 <= tile_id <= MAXOTHTILE
        return self.tiles[tile_id]

    def _glyph_to_rgb(self, glyphs):
        # TODO this can probably be imporved
        # Expects glhyphs as two-dimensional numpy ndarray
        cols = None
        col = None

        for i in range(glyphs.shape[1]):
            for j in range(glyphs.shape[0]):
                rgb = self.glyph_id_to_rgb(glyphs[j, i])
                if col is None:
                    col = rgb
                else:
                    col = np.concatenate((col, rgb))

            if cols is None:
                cols = col
            else:
                cols = np.concatenate((cols, col), axis=1)
            col = None

        return cols

    def to_rgb(self, glyphs, chars):
        # Fix glyphs with 0 ID
        glyphs = glyphs.copy()  # we might change it
        zero_indices = np.argwhere(glyphs == 0)
        for i, j in zero_indices:
            if chars[i, j] == ord("a"):  # giant ant
                continue
            else:
                glyphs[i, j] = 2359  # dark part of the room

        return self._glyph_to_rgb(glyphs)
