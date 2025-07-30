import type { Layout, Data } from 'plotly.js';
import type { dh as DhType } from '@deephaven/jsapi-types';
import { Formatter } from '@deephaven/jsapi-utils';
import { ChartModel, ChartUtils, FilterColumnMap, FilterMap } from '@deephaven/chart';
import { ChartEvent, RenderOptions } from '@deephaven/chart/dist/ChartModel';
import memoize from 'memoizee';
import { DownsampleInfo, PlotlyChartWidgetData, FormatUpdate } from './PlotlyExpressChartUtils';
export declare class PlotlyExpressChartModel extends ChartModel {
    /**
     * The size at which the chart will automatically downsample the data if it can be downsampled.
     * If it cannot be downsampled, but the size is below MAX_FETCH_SIZE,
     * the chart will show a confirmation to fetch the data since it might be a slow operation.
     */
    static AUTO_DOWNSAMPLE_SIZE: number;
    /**
     * The maximum number of items that can be fetched from a table.
     * If a table is larger than this, the chart will not be fetched.
     * This is to prevent the chart from fetching too much data and crashing the browser.
     */
    static MAX_FETCH_SIZE: number;
    static canFetch(table: DhType.Table): boolean;
    constructor(dh: typeof DhType, widget: DhType.Widget, refetch: () => Promise<DhType.Widget>);
    isSubscribed: boolean;
    chartUtils: ChartUtils;
    refetch: () => Promise<DhType.Widget>;
    widget?: DhType.Widget;
    widgetUnsubscribe?: () => void;
    /**
     * Map of table index to Table object.
     */
    tableReferenceMap: Map<number, DhType.Table>;
    /**
     * Map of downsampled table indexes to original Table object.
     */
    downsampleMap: Map<number, DownsampleInfo>;
    /**
     * Map of table index to TableSubscription object.
     */
    tableSubscriptionMap: Map<number, DhType.TableSubscription>;
    /**
     * Map of table index to cleanup function for the subscription.
     */
    subscriptionCleanupMap: Map<number, () => void>;
    /**
     * Map of table index to map of column names to array of paths where the data should be replaced.
     */
    tableColumnReplacementMap: Map<number, Map<string, string[]>>;
    /**
     * Map of table index to ChartData object. Used to handle data delta updates.
     */
    chartDataMap: Map<number, DhType.plot.ChartData>;
    /**
     * Map of table index to object where the keys are column names and the values are arrays of data.
     * This data is the full array of data for the column since ChartData doesn't have a clean way to get it at any time.
     */
    tableDataMap: Map<number, {
        [key: string]: unknown[];
    }>;
    plotlyData: Data[];
    layout: Partial<Layout>;
    isPaused: boolean;
    hasPendingUpdate: boolean;
    hasInitialLoadCompleted: boolean;
    isDownsamplingDisabled: boolean;
    isWebGlSupported: boolean;
    /**
     * Set of traces that are originally WebGL and can be replaced with non-WebGL traces.
     * These need to be replaced if WebGL is disabled and re-enabled if WebGL is enabled again.
     */
    webGlTraceIndices: Set<number>;
    /**
     * The WebGl warning is only shown once per chart. When the user acknowledges the warning, it will not be shown again.
     */
    hasAcknowledgedWebGlWarning: boolean;
    /**
     * A calendar object that is used to set rangebreaks on a time axis.
     */
    calendar: DhType.calendar.BusinessCalendar | null;
    /**
     * The set of parameters that need to be replaced with the default value format.
     */
    defaultValueFormatSet: Set<FormatUpdate>;
    /**
     * Map of variable within the plotly data to type.
     * For example, '0/value' -> 'int'
     */
    dataTypeMap: Map<string, string>;
    /**
     * Map of filter column names to their metadata.
     */
    filterColumnMap: FilterColumnMap;
    /**
     * The filter map that is sent to the server.
     * This is a map of column names to filter values.
     */
    filterMap: FilterMap | null;
    /**
     * A set of column names that are required for the chart to render.
     * If any of these columns are not in the filter map, the chart will not render.
     */
    requiredColumns: Set<string>;
    getData(): Partial<Data>[];
    getLayout(): Partial<Layout>;
    close(): void;
    subscribe(callback: (event: ChartEvent) => void): Promise<void>;
    unsubscribe(callback: (event: ChartEvent) => void): void;
    setRenderOptions(renderOptions: RenderOptions): void;
    /**
     * Handle the WebGL option being set in the render options.
     * If WebGL is enabled, traces have their original types as given.
     * If WebGL is disabled, replace traces that require WebGL with non-WebGL traces if possible.
     * Also, show a dismissible warning per-chart if there are WebGL traces that cannot be replaced.
     * @param webgl The new WebGL value. True if WebGL is enabled.
     * @param prevWebgl The previous WebGL value
     */
    handleWebGlAllowed(webgl?: boolean, prevWebgl?: boolean): void;
    fireBlockerClear(isAcknowledged?: boolean): void;
    updateLayout(data: PlotlyChartWidgetData): void;
    /**
     * Check if the timezone has changed in the new formatter
     * @param formatter The new formatter
     * @returns True if the timezone has changed
     */
    timeZoneChanged(formatter: Formatter): boolean;
    /**
     * Update the calendar object from the data
     * @param data The new data to update the calendar from
     */
    updateCalendar(data: PlotlyChartWidgetData): void;
    /**
     * Fire an event to update the rangebreaks on the chart.
     * @param formatter The formatter to use to set the rangebreaks. If not provided, the current formatter is used.
     */
    fireRangebreaksUpdated(formatter?: Formatter | undefined): void;
    /**
     * Update the filter columns from the data.
  
     * @param data The new data to update the filter columns from
     */
    updateFilterColumns(data: PlotlyChartWidgetData): void;
    /**
     * Unsubscribe from a table.
     * @param id The table ID to unsubscribe from
     */
    unsubscribeTable(id: number): void;
    /**
     * Fire an event to update the timezone on the chart data if it has changed.
     * @param formatter The new formatter
     */
    fireTimeZoneUpdated(): void;
    setFormatter(formatter: Formatter): void;
    handleWidgetUpdated(data: PlotlyChartWidgetData, references: DhType.Widget['exportedObjects']): void;
    handleFigureUpdated(event: DhType.Event<DhType.SubscriptionTableData>, tableId: number): void;
    addTable(id: number, table: DhType.Table): Promise<void>;
    updateDownsampledTable(id: number): Promise<void>;
    setDownsamplingDisabled(isDownsamplingDisabled: boolean): void;
    /**
     * Gets info on how to downsample a table for plotting.
     * @param tableId The tableId to get downsample info for
     * @param table The table to get downsample info for
     * @returns DownsampleInfo if table can be downsampled.
     *          A string of the reason if the table cannot be downsampled.
     *          Null if the table does not need downsampling.
     */
    getDownsampleInfo(tableId: number, table: DhType.Table): DownsampleInfo | string;
    subscribeTable(id: number): void;
    removeTable(id: number): void;
    fireUpdate(data: unknown): void;
    setDimensions(rect: DOMRect): void;
    getFilterColumnMap(): FilterColumnMap;
    isFilterRequired(): boolean;
    setFilter(filterMap: FilterMap): void;
    /**
     * Fire an event to update the filters on the chart.
     * @param filterMap The filter map to send to the server
     */
    sendFilterUpdated(filterMap: FilterMap): void;
    pauseUpdates(): void;
    resumeUpdates(): void;
    shouldPauseOnUserInteraction(): boolean;
    hasScene(): boolean;
    hasGeo(): boolean;
    hasMapbox(): boolean;
    hasPolar(): boolean;
    getPlotWidth(): number;
    getPlotHeight(): number;
    getTimeZone: ((columnType: string, formatter: Formatter | undefined) => DhType.i18n.TimeZone | undefined) & memoize.Memoized<(columnType: string, formatter: Formatter | undefined) => DhType.i18n.TimeZone | undefined>;
    getValueTranslator: ((columnType: string, formatter: Formatter | undefined) => (value: unknown) => unknown) & memoize.Memoized<(columnType: string, formatter: Formatter | undefined) => (value: unknown) => unknown>;
}
export default PlotlyExpressChartModel;
//# sourceMappingURL=PlotlyExpressChartModel.d.ts.map