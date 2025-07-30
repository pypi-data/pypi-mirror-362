import { ChartUtils } from '@deephaven/chart';
/**
 * Traces that are at least partially powered by WebGL and have no SVG equivalent.
 * https://plotly.com/python/webgl-vs-svg/
 */
const UNREPLACEABLE_WEBGL_TRACE_TYPES = new Set([
    'splom',
    'parcoords',
    'scatter3d',
    'surface',
    'mesh3d',
    'cone',
    'streamtube',
    'scattermapbox',
    'choroplethmapbox',
    'densitymapbox',
]);
/*
 * A map of trace type to attributes that should be set to a single value instead
 * of an array in the Figure object. The attributes should be relative to the trace
 * within the plotly/data/ array.
 */
const SINGLE_VALUE_REPLACEMENTS = {
    indicator: new Set(['value', 'delta/reference', 'title/text']),
};
/**
 * A prefix for the number format to indicate it is in Java format and should be
 *  transformed to a d3 format
 */
export const FORMAT_PREFIX = 'DEEPHAVEN_JAVA_FORMAT=';
export function getWidgetData(widgetInfo) {
    return JSON.parse(widgetInfo.getDataAsString());
}
export function getDataMappings(widgetData) {
    const data = widgetData.figure;
    // Maps a reference index to a map of column name to an array of the paths where its data should be
    const tableColumnReplacementMap = new Map();
    data.deephaven.mappings.forEach(({ table: tableIndex, data_columns: dataColumns }) => {
        var _a;
        const existingColumnMap = (_a = tableColumnReplacementMap.get(tableIndex)) !== null && _a !== void 0 ? _a : new Map();
        tableColumnReplacementMap.set(tableIndex, existingColumnMap);
        // For each { columnName: [replacePaths] } in the object, add to the tableColumnReplacementMap
        Object.entries(dataColumns).forEach(([columnName, paths]) => {
            const existingPaths = existingColumnMap.get(columnName);
            if (existingPaths !== undefined) {
                existingPaths.push(...paths);
            }
            else {
                existingColumnMap.set(columnName, [...paths]);
            }
        });
    });
    return tableColumnReplacementMap;
}
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
export function removeColorsFromData(colorway, data) {
    const plotlyColors = new Set(colorway.map(color => color.toUpperCase()));
    // Just check if the colors are in the colorway at any point
    // Plotly has many different ways to layer/order series
    for (let i = 0; i < data.length; i += 1) {
        const trace = data[i];
        // There are multiple datatypes in plotly and some don't contain marker or marker.color
        if ('marker' in trace &&
            trace.marker != null &&
            'color' in trace.marker &&
            typeof trace.marker.color === 'string') {
            if (plotlyColors.has(trace.marker.color.toUpperCase())) {
                delete trace.marker.color;
            }
        }
        if ('line' in trace &&
            trace.line != null &&
            'color' in trace.line &&
            typeof trace.line.color === 'string') {
            if (plotlyColors.has(trace.line.color.toUpperCase())) {
                delete trace.line.color;
            }
        }
    }
}
/**
 * Gets the path parts from a path replacement string from the widget data.
 * The parts start with the plotly data array as the root.
 * E.g. /plotly/data/0/x -> ['0', 'x']
 * @param path The path from the widget data
 * @returns The path parts within the plotly data array
 */
export function getPathParts(path) {
    return path
        .split('/')
        .filter(part => part !== '' && part !== 'plotly' && part !== 'data');
}
/**
 * Checks if a plotly series is a line series without markers
 * @param data The plotly data to check
 * @returns True if the data is a line series without markers
 */
export function isLineSeries(data) {
    return ((data.type === 'scatter' || data.type === 'scattergl') &&
        data.mode === 'lines');
}
/**
 * Checks if a plotly axis type is automatically determined based on the data
 * @param axis The plotly axis to check
 * @returns True if the axis type is determined based on the data
 */
export function isAutoAxis(axis) {
    return axis.type == null || axis.type === '-';
}
/**
 * Checks if a plotly axis type is linear
 * @param axis The plotly axis to check
 * @returns True if the axis is a linear axis
 */
export function isLinearAxis(axis) {
    return axis.type === 'linear' || axis.type === 'date';
}
/**
 * Check if 2 axis ranges are the same
 * A null range indicates an auto range
 * @param range1 The first axis range options
 * @param range2 The second axis range options
 * @returns True if the range options describe the same range
 */
export function areSameAxisRange(range1, range2) {
    return ((range1 === null && range2 === null) ||
        (range1 != null &&
            range2 != null &&
            range1[0] === range2[0] &&
            range1[1] === range2[1]));
}
export function downsample(dh, info) {
    var _a;
    return dh.plot.Downsample.runChartDownsample(info.originalTable, info.xCol, info.yCols, info.width, (_a = info.range) === null || _a === void 0 ? void 0 : _a.map(val => info.rangeType === 'date'
        ? dh.DateWrapper.ofJsDate(new Date(val))
        : dh.LongWrapper.ofString(val)));
}
/**
 * Get the indexes of the replaceable WebGL traces in the data
 * A replaceable WebGL has a type that ends with 'gl' which indicates it has a SVG equivalent
 * @param data The data to check
 * @returns The indexes of the WebGL traces
 */
export function getReplaceableWebGlTraceIndices(data) {
    const webGlTraceIndexes = new Set();
    data.forEach((trace, index) => {
        if (trace.type && trace.type.endsWith('gl')) {
            webGlTraceIndexes.add(index);
        }
    });
    return webGlTraceIndexes;
}
/**
 * Check if the data contains any traces that are at least partially powered by WebGL and have no SVG equivalent.
 * @param data The data to check for WebGL traces
 * @returns True if the data contains any unreplaceable WebGL traces
 */
export function hasUnreplaceableWebGlTraces(data) {
    return data.some(trace => trace.type && UNREPLACEABLE_WEBGL_TRACE_TYPES.has(trace.type));
}
/**
 * Set traces to use WebGL if WebGL is enabled and the trace was originally WebGL
 * or swap out WebGL for SVG if WebGL is disabled and the trace was originally WebGL
 * @param data The plotly figure data to update
 * @param webgl True if WebGL is enabled
 * @param webGlTraceIndices The indexes of the traces that are originally WebGL traces
 */
export function setWebGlTraceType(data, webgl, webGlTraceIndices) {
    webGlTraceIndices.forEach(index => {
        const trace = data[index];
        if (webgl && trace.type && !trace.type.endsWith('gl')) {
            // If WebGL is enabled and the trace is not already a WebGL trace, make it one
            trace.type = `${trace.type}gl`;
        }
        else if (!webgl && trace.type && trace.type.endsWith('gl')) {
            // If WebGL is disabled and the trace is a WebGL trace, remove the 'gl'
            trace.type = trace.type.substring(0, trace.type.length - 2);
        }
    });
}
/**
 * Create rangebreaks from a business calendar
 * @param formatter The formatter to use for the rangebreak calculations
 * @param calendar The business calendar to create the rangebreaks from
 * @param layout The layout to update with the rangebreaks
 * @param chartUtils The chart utils to use for the rangebreaks
 * @returns The updated layout with the rangebreaks added
 */
export function setRangebreaksFromCalendar(formatter, calendar, layout, chartUtils) {
    if (formatter != null && calendar != null) {
        const layoutUpdate = {};
        Object.keys(layout)
            .filter(key => key.includes('axis'))
            .forEach(key => {
            var _a;
            const axis = layout[key];
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            const rangebreaks = (_a = axis === null || axis === void 0 ? void 0 : axis.rangebreaks) !== null && _a !== void 0 ? _a : [];
            const updatedRangebreaks = chartUtils.createRangeBreaksFromBusinessCalendar(calendar, formatter);
            const updatedAxis = Object.assign(Object.assign({}, (typeof axis === 'object' ? axis : {})), { rangebreaks: [...rangebreaks, ...updatedRangebreaks] });
            layoutUpdate[key] = updatedAxis;
        });
        return layoutUpdate;
    }
    return null;
}
/**
 * Check if the data at the selector should be replaced with a single value instead of an array
 * @param data The data to check
 * @param selector The selector to check
 * @returns True if the data at the selector should be replaced with a single value
 */
export function isSingleValue(data, selector) {
    var _a, _b;
    const index = parseInt(selector[0], 10);
    const type = data[index].type;
    const path = selector.slice(1).join('/');
    return (_b = (_a = SINGLE_VALUE_REPLACEMENTS[type]) === null || _a === void 0 ? void 0 : _a.has(path)) !== null && _b !== void 0 ? _b : false;
}
/**
 * Set the default value formats for all traces that require it
 * @param plotlyData The plotly data to update
 * @param defaultValueFormatSet The set of updates to make
 * @param dataTypeMap The map of path to column type to pull the correct default format from
 * @param formatter The formatter to use to get the default format
 */
export function setDefaultValueFormat(plotlyData, defaultValueFormatSet, dataTypeMap, formatter = null) {
    defaultValueFormatSet.forEach(({ index, path, typeFrom, options }) => {
        const types = typeFrom.map(type => dataTypeMap.get(`${index}/${type}`));
        let columnType = null;
        if (types.some(type => type === 'double')) {
            // if any of the types are decimal, use decimal since it's the most specific
            columnType = 'double';
        }
        else if (types.some(type => type === 'int')) {
            columnType = 'int';
        }
        if (columnType == null) {
            return;
        }
        const typeFormatter = formatter === null || formatter === void 0 ? void 0 : formatter.getColumnTypeFormatter(columnType);
        if (typeFormatter == null || !('defaultFormatString' in typeFormatter)) {
            return;
        }
        const valueFormat = typeFormatter.defaultFormatString;
        if (valueFormat == null) {
            return;
        }
        const trace = plotlyData[index];
        // This object should be safe to cast to PlotNumber or Delta due
        // to the checks when originally added to the set
        const convertData = trace[path];
        convertToPlotlyNumberFormat(convertData, valueFormat, options);
    });
}
/**
 * Convert the number format to a d3 number format
 * @param data The data to update
 * @param valueFormat The number format to convert to a d3 format
 * @param options Options of what to update
 */
export function convertToPlotlyNumberFormat(data, valueFormat, options = {}) {
    var _a, _b, _c;
    // by default, everything should be updated dependent on updateFormat
    const updateFormat = (_a = options === null || options === void 0 ? void 0 : options.format) !== null && _a !== void 0 ? _a : true;
    const updatePrefix = (_b = options === null || options === void 0 ? void 0 : options.prefix) !== null && _b !== void 0 ? _b : updateFormat;
    const updateSuffix = (_c = options === null || options === void 0 ? void 0 : options.suffix) !== null && _c !== void 0 ? _c : updateFormat;
    const formatResults = ChartUtils.getPlotlyNumberFormat(null, '', valueFormat);
    if (updateFormat &&
        (formatResults === null || formatResults === void 0 ? void 0 : formatResults.tickformat) != null &&
        (formatResults === null || formatResults === void 0 ? void 0 : formatResults.tickformat) !== '') {
        // eslint-disable-next-line no-param-reassign
        data.valueformat = formatResults.tickformat;
    }
    if (updatePrefix) {
        // there may be no prefix now, so remove the preexisting one
        // eslint-disable-next-line @typescript-eslint/no-explicit-any, no-param-reassign
        data.prefix = '';
        // prefix and suffix might already be set, which should take precedence
        if ((formatResults === null || formatResults === void 0 ? void 0 : formatResults.tickprefix) != null && (formatResults === null || formatResults === void 0 ? void 0 : formatResults.tickprefix) !== '') {
            // eslint-disable-next-line no-param-reassign, @typescript-eslint/no-explicit-any
            data.prefix = formatResults.tickprefix;
        }
    }
    if (updateSuffix) {
        // eslint-disable-next-line @typescript-eslint/no-explicit-any, no-param-reassign
        data.suffix = '';
        // prefix and suffix might already be set, which should take precedence
        if ((formatResults === null || formatResults === void 0 ? void 0 : formatResults.ticksuffix) != null && (formatResults === null || formatResults === void 0 ? void 0 : formatResults.ticksuffix) !== '') {
            // eslint-disable-next-line no-param-reassign, @typescript-eslint/no-explicit-any
            data.suffix = formatResults.ticksuffix;
        }
    }
}
/**
 * Transform the number format to a d3 number format, which is used by Plotly
 * @param numberFormat The number format to transform
 * @returns The d3 number format
 */
export function transformValueFormat(data) {
    let valueFormat = data === null || data === void 0 ? void 0 : data.valueformat;
    if (valueFormat == null) {
        // if there's no format, note this so that the default format can be used
        // prefix and suffix should only be updated if the default format is used and they are not already set
        return {
            format: true,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            prefix: (data === null || data === void 0 ? void 0 : data.prefix) == null,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            suffix: (data === null || data === void 0 ? void 0 : data.suffix) == null,
        };
    }
    if (valueFormat.startsWith(FORMAT_PREFIX)) {
        valueFormat = valueFormat.substring(FORMAT_PREFIX.length);
    }
    else {
        // don't transform if it's not a deephaven format
        return {
            format: false,
        };
    }
    // transform once but don't transform again, so false is returned for format
    const options = {
        format: true,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        prefix: (data === null || data === void 0 ? void 0 : data.prefix) == null,
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        suffix: (data === null || data === void 0 ? void 0 : data.suffix) == null,
    };
    convertToPlotlyNumberFormat(data, valueFormat, options);
    return {
        format: false,
    };
}
/**
 * Replace the number formats in the data with a d3 number format
 * @param data The data to update
 */
export function replaceValueFormat(plotlyData) {
    const defaultValueFormatSet = new Set();
    plotlyData.forEach((trace, i) => {
        if (trace.type === 'indicator') {
            if ((trace === null || trace === void 0 ? void 0 : trace.number) == null) {
                // eslint-disable-next-line no-param-reassign
                trace.number = {};
            }
            const numberFormatOptions = transformValueFormat(trace.number);
            if (numberFormatOptions.format) {
                defaultValueFormatSet.add({
                    index: i,
                    path: 'number',
                    typeFrom: ['value', 'delta/reference'],
                    options: numberFormatOptions,
                });
            }
            if ((trace === null || trace === void 0 ? void 0 : trace.delta) == null) {
                // eslint-disable-next-line no-param-reassign
                trace.delta = {};
            }
            const deltaFormatOptions = transformValueFormat(trace.delta);
            if (deltaFormatOptions.format) {
                defaultValueFormatSet.add({
                    index: i,
                    path: 'delta',
                    typeFrom: ['value', 'delta/reference'],
                    options: deltaFormatOptions,
                });
            }
        }
    });
    return defaultValueFormatSet;
}
/**
 * Get the types of variables assocated with columns in the data
 * For example, if the path /plotly/data/0/value is associated with a column of type int,
 * the map will have the entry '0/value' -> 'int'
 * @param deephavenData The deephaven data from the widget to get path and column name from
 * @param tableReferenceMap The map of table index to table reference.
 * Types are pulled from the table reference
 * @returns A map of path to column type
 */
export function getDataTypeMap(deephavenData, tableReferenceMap) {
    const dataTypeMap = new Map();
    const { mappings } = deephavenData;
    mappings.forEach(({ table: tableIndex, data_columns: dataColumns }) => {
        const table = tableReferenceMap.get(tableIndex);
        Object.entries(dataColumns).forEach(([columnName, paths]) => {
            const column = table === null || table === void 0 ? void 0 : table.findColumn(columnName);
            if (column == null) {
                return;
            }
            const columnType = column.type;
            paths.forEach(path => {
                const cleanPath = getPathParts(path).join('/');
                dataTypeMap.set(cleanPath, columnType);
            });
        });
    });
    return dataTypeMap;
}
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
export function isWebGLSupported() {
    try {
        // https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/By_example/Detect_WebGL
        const canvas = document.createElement('canvas');
        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
        return gl != null && gl instanceof WebGLRenderingContext;
    }
    catch (e) {
        return false;
    }
}
export const IS_WEBGL_SUPPORTED = isWebGLSupported();
//# sourceMappingURL=PlotlyExpressChartUtils.js.map