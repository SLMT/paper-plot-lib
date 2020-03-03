import csv
import matplotlib.pyplot as plt
import numpy as np

# =============
#   Constants
# =============

# Figure types
FIG_LINES = 1
FIG_STACKS = 2
FIG_GROUP_BARS = 3

# ===================
#   Direct Builders
# ===================

def lines(x, ys, figsize=(-1, -1)):
    return FigureBuilder((x, ys), FIG_LINES, figsize)

def stacks(data, figsize=(-1, -1)):
    return FigureBuilder(data, FIG_STACKS, figsize)

def group_bars(data, figsize=(-1, -1)):
    return FigureBuilder(data, FIG_GROUP_BARS, figsize)

# ====================
#   CSV Constructors
# ====================

# Assumptions:
# 1: there is a header line
# 2: the first column is x
# 3: all values are integers

def lines_from_csv(filename, figsize=(-1, -1)):
    x_label = ''
    line_labels = []
    x_data = []
    line_data = []

    # Read data
    with open(filename, 'r') as f:
        for row in csv.reader(f):
            if x_label == '':
                x_label = row[0]
                line_labels = row[1:]
                for i in range(len(line_labels)):
                    line_data.append([])
            else:
                if row[0] == '':
                    continue
                x_data.append(convert_to_number(row[0]))
                for i in range(len(line_labels)):
                    line_data[i].append(convert_to_number(row[i + 1]))
    
    return lines(x_data, line_data, figsize).x_label(x_label).data_labels(line_labels)

def stacks_from_csv(filename, figsize=(-1, -1)):
    return group_bars_from_csv(filename, figsize).change_figure_type(FIG_STACKS)

def group_bars_from_csv(filename, figsize=(-1, -1)):
    x_labels = []
    bar_labels = []
    bar_data = []

    # Read data
    with open(filename, 'r') as f:
        for row in csv.reader(f):
            if len(bar_labels) == 0:
                bar_labels = row[1:]
                for i in range(len(bar_labels)):
                    bar_data.append([])
            else:
                if row[0] == '':
                    continue
                x_labels.append(row[0])
                for i in range(len(bar_labels)):
                    bar_data[i].append(convert_to_number(row[i + 1]))

    return group_bars(bar_data, figsize).group_labels(x_labels).data_labels(bar_labels)

# ================
#   Main Builder
# ================

class FigureBuilder:
    def __init__(self, data, figure_type, figsize=(-1, -1)):
        self.data = data
        self.fig_type = figure_type
        self.fig_size = figsize
        self.fig_has_drawn = False
        self.axe_x_label = ''
        self.axe_x_label_size = 12
        self.axe_y_label = ''
        self.axe_y_label_size = 12
        self.axe_data_labels = []
        self.axe_group_labels = []
        self.axe_tick_size = 12
        self.axe_x_ticks = []
        self.axe_x_ticks_labels = []
        self.axe_legend_on = False
        self.axe_legend_out = False
        self.axe_legend_pos = 'lower right'
        self.axe_legend_size = 12
        self.axe_data_colors = []
        self.axe_line_markers = []
        self.axe_line_styles = []
        self.vlines = []

    def change_figure_type(self, new_type):
        if self.fig_type == FIG_GROUP_BARS and new_type == FIG_STACKS:
            self.fig_type = FIG_STACKS
        else:
            raise ValueError('Cannot change type from {} to {}'.format(self.fig_type, new_type))
        return self

    def x_label(self, label_name):
        self.axe_x_label = label_name
        return self

    def x_label_size(self, size):
        self.axe_x_label_size = size
        return self

    def y_label(self, label_name):
        self.axe_y_label = label_name
        return self

    def y_label_size(self, size):
        self.axe_y_label_size = size
        return self

    def data_labels(self, label_names):
        self.axe_data_labels = label_names
        self.axe_legend_ncol = len(self.axe_data_labels)
        return self

    def group_labels(self, label_names):
        self.axe_group_labels = label_names
        return self

    def legend_size(self, size):
        if len(self.axe_data_labels) == 0:
            raise ValueError("data labels must be set before using legends")

        self.axe_legend_on = True
        self.axe_legend_size = size
        return self

    def legend_ncol(self, ncol):
        if len(self.axe_data_labels) == 0:
            raise ValueError("data labels must be set before using legends")

        self.axe_legend_on = True
        self.axe_legend_ncol = ncol
        return self
        
    def x_ticks(self, values):
        self.axe_x_ticks = values
        return self
        
    def x_ticks_labels(self, labels):
        self.axe_x_ticks_labels = labels
        return self

    def tick_size(self, size):
        self.axe_tick_size = size
        return self

    def label_size(self, size):
        self.x_label_size(size)
        self.y_label_size(size)
        return self 
        
    def x_min(self, val):
        self.axe_x_min = val
        return self

    def x_max(self, val):
        self.axe_x_max = val
        return self
        
    def y_min(self, val):
        self.axe_y_min = val
        return self

    def y_max(self, val):
        self.axe_y_max = val
        return self
        
    def x_scale(self, val):
        self.axe_xscale = val
        return self

    def y_scale(self, val):
        self.axe_yscale = val
        return self

    def show_legend(self):
        self.axe_legend_on = True
        return self

    def legend_out(self):
        if len(self.axe_data_labels) == 0:
            raise ValueError("data labels must be set before using legends")
        
        self.axe_legend_on = True
        self.axe_legend_out = True
        return self

    def markers(self, markers):
        self.axe_line_markers = markers
        return self

    def colors(self, colors):
        self.axe_data_colors = colors
        return self

    def line_styles(self, line_styles):
        self.axe_line_styles = line_styles
        return self

    def add_vline(self, x, color='black', linestyle='-'):
        self.vlines.append((x, color, linestyle))
        return self

    def draw(self):
        # Create a figure
        if self.fig_size == (-1, -1):
            (fig, axe) = plt.subplots(1, 1)
        else:
            (fig, axe) = plt.subplots(1, 1, figsize=self.fig_size)

        # Draw on the figure
        # Lines
        if self.fig_type == FIG_LINES:
            x = self.data[0]
            ys = self.data[1]

            lines = []
            for y in ys:
                lines_handle = axe.plot(x, y)
                lines.append(lines_handle[0])
            axe.set_xlim(x[0], x[-1])

            # Markers
            if len(self.axe_line_markers) > 0:
                for i in range(len(lines)):
                    lines[i].set_marker(self.axe_line_markers[i])

            # Line styles
            if len(self.axe_line_styles) > 0:
                for i in range(len(lines)):
                    lines[i].set_linestyle(self.axe_line_styles[i])

            # Color
            if len(self.axe_data_colors) > 0:
                for i in range(len(lines)):
                    lines[i].set_color(self.axe_data_colors[i])
        
        # Group Bars & Stacks
        elif self.fig_type == FIG_GROUP_BARS or self.fig_type == FIG_STACKS:
            bar_data = self.data

            # Draw bars
            if self.fig_type == FIG_GROUP_BARS:
                x = np.arange(len(bar_data[0]))  # the label locations
                bar_count = len(bar_data)
                width = 0.8 / bar_count  # the width of the bars
                x_left = x - width * bar_count / 2 + width / 2
                bars = []
                for i in range(len(bar_data)):
                    if len(self.axe_data_colors) > 0:
                        bar = axe.bar(x_left + width * i, bar_data[i], width, color=self.axe_data_colors[i])
                    else:
                        bar = axe.bar(x_left + width * i, bar_data[i], width)
                    bars.append(bar)
            elif self.fig_type == FIG_STACKS:
                x = np.arange(len(bar_data[0]))  # the label locations
                sums = np.zeros(len(bar_data[0]))
                bars = []
                for i in range(len(bar_data)):
                    if len(self.axe_data_colors) > 0:
                        bar = axe.bar(x, bar_data[i], width=0.5, bottom=sums, color=self.axe_data_colors[i])
                    else:
                        bar = axe.bar(x, bar_data[i], width=0.5, bottom=sums)
                    sums += bar_data[i]
                    bars.append(bar)
            
            # Set data labels
            if len(self.axe_data_labels) > 0:
                for i in range(len(bars)):
                    bars[i].set_label(self.axe_data_labels[i])

            # Set group labels
            if len(self.axe_group_labels) > 0:
                axe.set_xticks(range(len(self.axe_group_labels)))
                axe.set_xticklabels(self.axe_group_labels)
        
        # Draw other information
        if self.axe_x_label != '':
            axe.set_xlabel(self.axe_x_label, fontsize=self.axe_x_label_size)
        if self.axe_y_label != '':
            axe.set_ylabel(self.axe_y_label, fontsize=self.axe_y_label_size)
        axe.tick_params(axis='both', which='both', labelsize=self.axe_tick_size)
        if len(self.axe_x_ticks) > 0:
            axe.set_xticks(self.axe_x_ticks)
        if len(self.axe_x_ticks_labels) > 0:
            axe.set_xticklabels(self.axe_x_ticks_labels)
        if hasattr(self, 'axe_x_min'):
            axe.set_xlim(left=self.axe_x_min)
        if hasattr(self, 'axe_x_max'):
            axe.set_xlim(right=self.axe_x_max)
        if hasattr(self, 'axe_y_min'):
            axe.set_ylim(bottom=self.axe_y_min)
        if hasattr(self, 'axe_y_max'):
            axe.set_ylim(top=self.axe_y_max)
        if hasattr(self, 'axe_xscale'):
            axe.set_xscale(self.axe_xscale)
        if hasattr(self, 'axe_yscale'):
            axe.set_yscale(self.axe_yscale)

        # Add vertical lines
        (ymin, ymax) = axe.get_ylim()
        for (x, color, style) in self.vlines:
            axe.vlines(x=x, ymin=ymin, ymax=ymax, color=color, linestyle=style)

        # Legend
        if self.axe_legend_on:
            if self.axe_legend_out:
                (w, h) = fig.get_size_inches()
                up_shfit = (0.75 / h) * (len(self.axe_data_labels) / self.axe_legend_ncol)
                axe.legend(self.axe_data_labels, loc='upper center', bbox_to_anchor=(0.45, 1 + up_shfit), \
                        prop={'size': self.axe_legend_size}, ncol=self.axe_legend_ncol, frameon=False)
            else:
                axe.legend(self.axe_data_labels, prop={'size': self.axe_legend_size}, loc=self.axe_legend_pos)

        # Size
        fig.subplots_adjust(bottom=0.2)

        # Save the fig
        self.fig = fig
        self.fig_has_drawn = True

        return self

    def save_as_pdf(self, filename):
        filename = filename.replace('.pdf', '')
        if not self.fig_has_drawn:
            self.draw()
        self.fig.savefig('{}.pdf'.format(filename), dpi=300, bbox_inches='tight')
        return self

# =====================
#   Utility Functions
# =====================

def convert_to_number(string):
    return float(string)
    # return int(string, 10)
