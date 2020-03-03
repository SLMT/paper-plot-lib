# Paper Plot

A Python library that helps you plot figures that are put on your paper for your experiment results.

## Requirements

Python libraries:

- csv
- matplotlib
- numpy

## Examples

```python
import paper_plot as pt

pt.lines_from_csv('inputs/introduction.csv', figsize=(10, 3)) \
    .y_label('Throughput\n(K txs/15 secs)').tick_size(15).label_size(18)\
    .line_styles([':', '--', '-']).legend_size(17).legend_out() \
    .legend_ncol(3) \
    .draw().save_as_pdf('outputs/fig-ex-introduction')
```

![ex1](images/ex1.png)
