#  SPDX-FileCopyrightText: © 2022 Josef Hahn
#  SPDX-License-Identifier: AGPL-3.0-only
import datetime
import sys
import traceback
import typing as t
import viwid.widgets.widget


class Layout:

    def set_size(self, value):
        pass

    def compute_width(self, minimal: bool):
        pass

    def compute_height(self, width, minimal: bool):
        pass


class NullLayout:

    def set_size(self, value):
        pass

    def compute_width(self, minimal):
        raise Exception("TODO")

    def compute_height(self, width, minimal):
        raise Exception("TODO")


TPartitioning = list[list["viwid.widgets.widget.Widget"]]


class GridLayout(Layout):

    def __init__(self, partitioning: t.Callable[[], TPartitioning]):
        self.__partitioning = lambda: list(partitioning())

    @staticmethod
    def __stretch_from_partitioning(partitioning: TPartitioning):
        stretch_cols = [False for x in partitioning[0]] if (len(partitioning) > 0) else []
        stretch_rows = [False for x in partitioning]
        for r, row in enumerate(partitioning):
            for c, cell in enumerate(row):
                if cell.computed_vertical_expand_greedily:
                    stretch_rows[r] = True
                if cell.computed_horizontal_expand_greedily:
                    stretch_cols[c] = True
        return stretch_cols, stretch_rows

    @staticmethod
    def __horizontally_process_partitioning(partitioning: TPartitioning, minimal):
        cols = [0 for x in partitioning[0]] if (len(partitioning) > 0) else []
        computed_widths = {}
        for r, row in enumerate(partitioning):
            for c, cell in enumerate(row):
                w = cell.compute_width2(minimal)
                computed_widths[cell] = w
                cols[c] = max(cols[c], w)
        return cols, computed_widths

    @staticmethod
    def __vertically_process_partitioning(partitioning: TPartitioning, minimal, cols: list[int]):
        rows = [0 for x in partitioning]
        computed_heights = {}
        for r, row in enumerate(partitioning):
            for c, cell in enumerate(row):
                h = cell.compute_height2(cols[c], minimal)
                computed_heights[cell] = h
                rows[r] = max(rows[r], h)
        return rows, computed_heights

    @staticmethod
    def __stretch_axis_minimals(axis, axis_minimal, target_size):
        deltaw = max(0, target_size - sum(axis_minimal))
        deltam = sum(axis) - sum(axis_minimal)
        if deltam > 0 and deltaw > 0:
            fact = max(0, min(1, deltaw / deltam))
            acols = []
            for icc, cc in enumerate(axis_minimal):
                mydf = axis[icc] - cc
                acols.append(cc + int(fact * (mydf)))
            return acols
        return axis_minimal

    @staticmethod
    def __stretch_axis_finally(axis, stretch_axis, target_size):
        axis = list(axis)
        wdiff = target_size - sum(axis)
        if wdiff > 0:  # TODO elif <0 ?!
            istarcols = [i for i, x in enumerate(stretch_axis) if x]
            nstarcols = len(istarcols)
            if nstarcols > 0:
                xwdiff = int(wdiff / nstarcols)
                for i in reversed(range(nstarcols)):
                    ii = istarcols[i]
                    if i:
                        axis[ii] += xwdiff
                    else:
                        axis[ii] += (wdiff - (xwdiff * (nstarcols - 1)))
        return axis

    @staticmethod
    def __process_partitioning(partitioning, size, fuh=None):
        stretch_cols, stretch_rows = GridLayout.__stretch_from_partitioning(partitioning)
        pcols, computed_widths = GridLayout.__horizontally_process_partitioning(partitioning, False)
        if size.width < sum(pcols):
            cols, computed_widths_ = GridLayout.__horizontally_process_partitioning(partitioning, True)
            cols = GridLayout.__stretch_axis_minimals(pcols, cols, size.width)
        else:
            cols = pcols
        cols = GridLayout.__stretch_axis_finally(cols, stretch_cols, size.width)
        prows, computed_heights = GridLayout.__vertically_process_partitioning(partitioning, False, cols)
        if (size.height < sum(prows)) or (fuh is True):
            rows = prows
            if (fuh is not False):
                rows, computed_heights_ = GridLayout.__vertically_process_partitioning(partitioning, True, cols)
            if (fuh is None):
                rows = GridLayout.__stretch_axis_minimals(prows, rows, size.height)
        else:
            rows = prows
        if (fuh is None):
            rows = GridLayout.__stretch_axis_finally(rows, stretch_rows, size.height)
        return cols, rows, partitioning, {w: viwid.Size(wi,computed_heights[w]) for w,wi in computed_widths.items()}

    def __trim_geometry(self, position, size, total_size):
        position = viwid.Point(min(position.x, total_size.width), min(position.y, total_size.height))
        size = viwid.Size(min(size.width, total_size.width-position.x),
                          min(size.height, total_size.height-position.y))
        return position, size

    def compute_width(self, minimal: bool) -> int:
        partitioning = self.__partitioning()
        cols, computed_widths = self.__horizontally_process_partitioning(partitioning, minimal)
        self.__vertically_process_partitioning(partitioning, minimal, cols)
        return sum(cols)

    def compute_height(self, width: int, minimal: bool) -> int:
        partitioning = self.__partitioning()
        geometry = self.__process_partitioning(partitioning, viwid.Size(width, 0), fuh=minimal)
        return sum(geometry[1])

    def set_size(self, value):
        partitioning = self.__partitioning()
        geometry = self.__process_partitioning(partitioning, value)
        y = 0
        Alignment = viwid.widgets.widget.Alignment
        for r, rowline in enumerate(geometry[2]):
            x = 0
            for c, child in enumerate(rowline):
                box = viwid.Size(geometry[0][c], geometry[1][r])
                boxp = viwid.Point(x, y)
                natsiz = geometry[3][child]
                xx = child.vertical_alignment
                if xx is None:
                    xx = Alignment.FILL if child.computed_vertical_expand_greedily else Alignment.CENTER
                if xx != Alignment.FILL:
                    hdiffsiz = int( (box.height - natsiz.height) / 2)
                    if hdiffsiz > 0:
                        if xx == Alignment.START:
                            pass
                        elif xx == Alignment.CENTER:
                            boxp = boxp.moved_by(y=hdiffsiz)
                        elif xx == Alignment.STOP:
                            boxp = boxp.moved_by(y=box.height-natsiz.height)
                        box = box.with_height(natsiz.height)
                xx = child.horizontal_alignment
                if xx is None:
                    xx = Alignment.FILL if child.computed_horizontal_expand_greedily else Alignment.CENTER
                if xx != Alignment.FILL:
                    hdiffsiz =int(  (box.width - natsiz.width) / 2)
                    if hdiffsiz > 0:
                        if xx == Alignment.START:
                            pass
                        elif xx == Alignment.CENTER:
                            boxp = boxp.moved_by(x=hdiffsiz)
                        elif xx == Alignment.STOP:
                            boxp = boxp.moved_by(x=box.width - natsiz.width)
                        box = box.with_width(natsiz.width)
                boxp, box = self.__trim_geometry(boxp, box, value)
                child.set_position(boxp)
                child.set_size(box)
                x += geometry[0][c]
            y += geometry[1][r]
