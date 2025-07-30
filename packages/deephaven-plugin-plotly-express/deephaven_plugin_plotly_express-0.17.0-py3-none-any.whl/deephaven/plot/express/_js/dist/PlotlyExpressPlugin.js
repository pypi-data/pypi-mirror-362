import { PluginType } from '@deephaven/plugin';
import { vsGraph } from '@deephaven/icons';
import { PlotlyExpressChart } from './PlotlyExpressChart.js';
import { PlotlyExpressChartPanel } from './PlotlyExpressChartPanel.js';
export const PlotlyExpressPlugin = {
    name: '@deephaven/plotly-express',
    type: PluginType.WIDGET_PLUGIN,
    supportedTypes: 'deephaven.plot.express.DeephavenFigure',
    component: PlotlyExpressChart,
    panelComponent: PlotlyExpressChartPanel,
    icon: vsGraph,
};
export default PlotlyExpressPlugin;
//# sourceMappingURL=PlotlyExpressPlugin.js.map