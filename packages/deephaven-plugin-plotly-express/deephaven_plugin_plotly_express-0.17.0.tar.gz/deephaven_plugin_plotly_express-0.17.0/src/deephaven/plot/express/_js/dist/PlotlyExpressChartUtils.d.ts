import { type Data, type Delta, type LayoutAxis, type PlotlyDataLayoutConfig, type PlotNumber, type Layout } from 'plotly.js';
import type { dh as DhType } from '@deephaven/jsapi-types';
import { ChartUtils } from '@deephaven/chart';
import { Formatter } from '@deephaven/jsapi-utils';
/**
 * A prefix for the number format to indicate it is in Java format and should be
 *  transformed to a d3 format
 */
export declare const FORMAT_PREFIX = "DEEPHAVEN_JAVA_FORMAT=";
export interface PlotlyChartWidget {
    getDataAsBase64: () => string;
    exportedObjects: {
        fetch: () => Promise<DhType.Table>;
    }[];
    addEventListener: (type: string, fn: (event: CustomEvent<PlotlyChartWidget>) => () => void) => void;
}
interface DeephavenCalendarBusinessPeriod {
    open: string;
    close: string;
}
export interface FilterColumns {
    columns: Array<{
        type: string;
        name: string;
        required: boolean;
    }>;
}
export interface PlotlyChartDeephavenData {
    calendar?: {
        timeZone: string;
        businessDays: Array<string>;
        holidays: Array<{
            date: string;
            businessPeriods: Array<DeephavenCalendarBusinessPeriod>;
        }>;
        businessPeriods: Array<DeephavenCalendarBusinessPeriod>;
        name: string;
    };
    filterColumns?: FilterColumns;
    mappings: Array<{
        table: number;
        data_columns: Record<string, string[]>;
    }>;
    is_user_set_template: boolean;
    is_user_set_color: boolean;
}
export interface PlotlyChartWidgetData {
    type: string;
    figure: {
        deephaven: PlotlyChartDeephavenData;
        plotly: PlotlyDataLayoutConfig;
    };
    revision: number;
    new_references: number[];
    removed_references: number[];
}
/** Information that is needed to update the default value format in the data
 * The index is relative to the plotly/data/ array
 * The path within the trace has the valueformat to update
 * The typeFrom is a path to a variable that is mapped to a column type
 * The options indicate if the prefix and suffix should be set
 */
export interface FormatUpdate {
    index: number;
    path: string;
    typeFrom: string[];
    options: Record<string, boolean>;
}
export declare function getWidgetData(widgetInfo: DhType.Widget): PlotlyChartWidgetData;
export declare function getDataMappings(widgetData: PlotlyChartWidgetData): Map<number, Map<string, string[]>>;
/**
 * Removes the default colors from the data
 * Data color is not removed if the user set the color specifically or the plot type sets it
 *
 * This only checks if the marker or line color is set to a color in the colorway.
 * This means it is not possible to change the order of the colorway and use the same colors.
 *
 * @param colorway The colorway from plotly
 * @param data The data to remove the colorway from. This will be mutated
 */
export declare function removeColorsFromData(colorway: string[], data: Data[]): void;
/**
 * Gets the path parts from a path replacement string from the widget data.
 * The parts start with the plotly data array as the root.
 * E.g. /plotly/data/0/x -> ['0', 'x']
 * @param path The path from the widget data
 * @returns The path parts within the plotly data array
 */
export declare function getPathParts(path: string): string[];
/**
 * Checks if a plotly series is a line series without markers
 * @param data The plotly data to check
 * @returns True if the data is a line series without markers
 */
export declare function isLineSeries(data: Data): boolean;
/**
 * Checks if a plotly axis type is automatically determined based on the data
 * @param axis The plotly axis to check
 * @returns True if the axis type is determined based on the data
 */
export declare function isAutoAxis(axis: Partial<LayoutAxis>): boolean;
/**
 * Checks if a plotly axis type is linear
 * @param axis The plotly axis to check
 * @returns True if the axis is a linear axis
 */
export declare function isLinearAxis(axis: Partial<LayoutAxis>): boolean;
/**
 * Check if 2 axis ranges are the same
 * A null range indicates an auto range
 * @param range1 The first axis range options
 * @param range2 The second axis range options
 * @returns True if the range options describe the same range
 */
export declare function areSameAxisRange(range1: unknown[] | null, range2: unknown[] | null): boolean;
export interface DownsampleInfo {
    type: 'linear';
    /**
     * The original table before downsampling.
     */
    originalTable: DhType.Table;
    /**
     * The x column to downsample.
     */
    xCol: string;
    /**
     * The y columns to downsample.
     */
    yCols: string[];
    /**
     * The width of the x-axis in pixels.
     */
    width: number;
    /**
     * The range of the x-axis. Null if set to autorange.
     */
    range: string[] | null;
    /**
     * If the range is a datae or number
     */
    rangeType: 'date' | 'number';
}
export declare function downsample(dh: typeof DhType, info: DownsampleInfo): Promise<DhType.Table>;
/**
 * Get the indexes of the replaceable WebGL traces in the data
 * A replaceable WebGL has a type that ends with 'gl' which indicates it has a SVG equivalent
 * @param data The data to check
 * @returns The indexes of the WebGL traces
 */
export declare function getReplaceableWebGlTraceIndices(data: Data[]): Set<number>;
/**
 * Check if the data contains any traces that are at least partially powered by WebGL and have no SVG equivalent.
 * @param data The data to check for WebGL traces
 * @returns True if the data contains any unreplaceable WebGL traces
 */
export declare function hasUnreplaceableWebGlTraces(data: Data[]): boolean;
/**
 * Set traces to use WebGL if WebGL is enabled and the trace was originally WebGL
 * or swap out WebGL for SVG if WebGL is disabled and the trace was originally WebGL
 * @param data The plotly figure data to update
 * @param webgl True if WebGL is enabled
 * @param webGlTraceIndices The indexes of the traces that are originally WebGL traces
 */
export declare function setWebGlTraceType(data: Data[], webgl: boolean, webGlTraceIndices: Set<number>): void;
/**
 * Create rangebreaks from a business calendar
 * @param formatter The formatter to use for the rangebreak calculations
 * @param calendar The business calendar to create the rangebreaks from
 * @param layout The layout to update with the rangebreaks
 * @param chartUtils The chart utils to use for the rangebreaks
 * @returns The updated layout with the rangebreaks added
 */
export declare function setRangebreaksFromCalendar(formatter: Formatter | null, calendar: DhType.calendar.BusinessCalendar | null, layout: Partial<Layout>, chartUtils: ChartUtils): Partial<Layout> | null;
/**
 * Check if the data at the selector should be replaced with a single value instead of an array
 * @param data The data to check
 * @param selector The selector to check
 * @returns True if the data at the selector should be replaced with a single value
 */
export declare function isSingleValue(data: Data[], selector: string[]): boolean;
/**
 * Set the default value formats for all traces that require it
 * @param plotlyData The plotly data to update
 * @param defaultValueFormatSet The set of updates to make
 * @param dataTypeMap The map of path to column type to pull the correct default format from
 * @param formatter The formatter to use to get the default format
 */
export declare function setDefaultValueFormat(plotlyData: Data[], defaultValueFormatSet: Set<FormatUpdate>, dataTypeMap: Map<string, string>, formatter?: Formatter | null): void;
/**
 * Convert the number format to a d3 number format
 * @param data The data to update
 * @param valueFormat The number format to convert to a d3 format
 * @param options Options of what to update
 */
export declare function convertToPlotlyNumberFormat(data: Partial<PlotNumber> | Partial<Delta>, valueFormat: string, options?: Record<string, boolean>): void;
/**
 * Transform the number format to a d3 number format, which is used by Plotly
 * @param numberFormat The number format to transform
 * @returns The d3 number format
 */
export declare function transformValueFormat(data: Partial<PlotNumber> | Partial<Delta>): Record<string, boolean>;
/**
 * Replace the number formats in the data with a d3 number format
 * @param data The data to update
 */
export declare function replaceValueFormat(plotlyData: Data[]): Set<FormatUpdate>;
/**
 * Get the types of variables assocated with columns in the data
 * For example, if the path /plotly/data/0/value is associated with a column of type int,
 * the map will have the entry '0/value' -> 'int'
 * @param deephavenData The deephaven data from the widget to get path and column name from
 * @param tableReferenceMap The map of table index to table reference.
 * Types are pulled from the table reference
 * @returns A map of path to column type
 */
export declare function getDataTypeMap(deephavenData: PlotlyChartDeephavenData, tableReferenceMap: Map<number, DhType.Table>): Map<string, string>;
/**
 * Check if WebGL is supported in the current environment.
 * Most modern browsers do support WebGL, but it's possible to disable it and it is also not available
 * in some headless environments, which can affect e2e tests.
 *
 * https://github.com/microsoft/playwright/issues/13146
 * https://bugzilla.mozilla.org/show_bug.cgi?id=1375585
 *
 * @returns True if WebGL is supported, false otherwise
 */
export declare function isWebGLSupported(): boolean;
export declare const IS_WEBGL_SUPPORTED: boolean;
export {};
//# sourceMappingURL=PlotlyExpressChartUtils.d.ts.map