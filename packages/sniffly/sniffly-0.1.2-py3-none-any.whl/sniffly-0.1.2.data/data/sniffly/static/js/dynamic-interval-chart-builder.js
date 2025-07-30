/***********************************************************************
 * Shared palette & grid-line color
 *********************************************************************/
const COLOR = {
  red:    { stroke: '#ef4444', fill: 'rgba(239,68,68,0.1)'  },
  blue:   { stroke: '#667eea', fill: 'rgba(102,126,234,0.1)' },
  orange: { stroke: '#f59e0b', fill: 'rgba(245,158,11,0.1)' },
  amber:  { stroke: '#ed8936', fill: 'rgba(237,137,54,0.1)' }
};
const GRID_COLOR = 'rgba(0,0,0,0.05)';

const withColor = (name, extra = {}) => ({
  borderColor:    COLOR[name].stroke,
  backgroundColor: COLOR[name].fill,
  ...extra
});

/***********************************************************************
 * Generic dynamic-interval chart builder
 *********************************************************************/
function makeDynamicIntervalChart({
  canvasId,
  labels,
  datasets,
  yScales,
  legendPos = 'top',
  tooltipExtra = {},
  optionOverrides = {},
  limitedBucketData,
  useHourlyInterval
}) {
  /* format bucket timestamp for hourly *or* daily data */
  const fmt = idx => {
    const b = limitedBucketData[idx];
    if (!b) {return '';}
    const p = b.timestamp.split('-').map(Number);
    const d = useHourlyInterval
      ? new Date(p[0], p[1] - 1, p[2], p[3])
      : new Date(p[0], p[1] - 1, p[2]);
    return d.toLocaleDateString('en-US', {
      weekday: 'short',
      year:    'numeric',
      month:   'short',
      day:     'numeric',
      hour:    useHourlyInterval ? 'numeric' : undefined,
      hour12:  true
    });
  };

  /* supply default grid colors if missing */
  Object.values(yScales).forEach(s => {
    s.grid ??= {};
    if (!s.grid.color) {s.grid.color = GRID_COLOR;}
  });

  const opts = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend:  { display: true, position: legendPos },
      tooltip: { callbacks: { title: ctx => fmt(ctx[0].dataIndex), ...tooltipExtra } }
    },
    scales: {
      x: {
        title: { display: true, text: 'Time' },
        grid:  { color: GRID_COLOR },
        ticks: {
          maxRotation: 45,
          minRotation: 0,
          autoSkip: false,
          callback(v) { return this.getLabelForValue(v) || ''; }
        }
      },
      ...yScales
    },
    ...optionOverrides
  };

  return new Chart(document.getElementById(canvasId), {
    type: 'line',
    data: { labels, datasets },
    options: opts
  });
}
