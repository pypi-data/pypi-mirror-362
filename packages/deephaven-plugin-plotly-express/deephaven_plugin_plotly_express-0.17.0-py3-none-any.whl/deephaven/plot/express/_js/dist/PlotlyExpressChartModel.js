import { ChartModel, ChartUtils, } from '@deephaven/chart';
import Log from '@deephaven/log';
import memoize from 'memoizee';
import { areSameAxisRange, downsample, getDataMappings, getPathParts, getReplaceableWebGlTraceIndices, getWidgetData, isAutoAxis, isLineSeries, isLinearAxis, removeColorsFromData, setWebGlTraceType, hasUnreplaceableWebGlTraces, isSingleValue, replaceValueFormat, setDefaultValueFormat, getDataTypeMap, IS_WEBGL_SUPPORTED, setRangebreaksFromCalendar, } from './PlotlyExpressChartUtils';
const log = Log.module('@deephaven/js-plugin-plotly-express.ChartModel');
export class PlotlyExpressChartModel extends ChartModel {
    static canFetch(table) {
        return table.size <= PlotlyExpressChartModel.MAX_FETCH_SIZE;
    }
    constructor(dh, widget, refetch) {
        super(dh);
        this.isSubscribed = false;
        /**
         * Map of table index to Table object.
         */
        this.tableReferenceMap = new Map();
        /**
         * Map of downsampled table indexes to original Table object.
         */
        this.downsampleMap = new Map();
        /**
         * Map of table index to TableSubscription object.
         */
        this.tableSubscriptionMap = new Map();
        /**
         * Map of table index to cleanup function for the subscription.
         */
        this.subscriptionCleanupMap = new Map();
        /**
         * Map of table index to map of column names to array of paths where the data should be replaced.
         */
        this.tableColumnReplacementMap = new Map();
        /**
         * Map of table index to ChartData object. Used to handle data delta updates.
         */
        this.chartDataMap = new Map();
        /**
         * Map of table index to object where the keys are column names and the values are arrays of data.
         * This data is the full array of data for the column since ChartData doesn't have a clean way to get it at any time.
         */
        this.tableDataMap = new Map();
        this.plotlyData = [];
        this.layout = {};
        this.isPaused = false;
        this.hasPendingUpdate = false;
        this.hasInitialLoadCompleted = false;
        this.isDownsamplingDisabled = false;
        this.isWebGlSupported = IS_WEBGL_SUPPORTED;
        /**
         * Set of traces that are originally WebGL and can be replaced with non-WebGL traces.
         * These need to be replaced if WebGL is disabled and re-enabled if WebGL is enabled again.
         */
        this.webGlTraceIndices = new Set();
        /**
         * The WebGl warning is only shown once per chart. When the user acknowledges the warning, it will not be shown again.
         */
        this.hasAcknowledgedWebGlWarning = false;
        /**
         * A calendar object that is used to set rangebreaks on a time axis.
         */
        this.calendar = null;
        /**
         * The set of parameters that need to be replaced with the default value format.
         */
        this.defaultValueFormatSet = new Set();
        /**
         * Map of variable within the plotly data to type.
         * For example, '0/value' -> 'int'
         */
        this.dataTypeMap = new Map();
        /**
         * Map of filter column names to their metadata.
         */
        this.filterColumnMap = new Map();
        /**
         * The filter map that is sent to the server.
         * This is a map of column names to filter values.
         */
        this.filterMap = null;
        /**
         * A set of column names that are required for the chart to render.
         * If any of these columns are not in the filter map, the chart will not render.
         */
        this.requiredColumns = new Set();
        this.getTimeZone = memoize((columnType, formatter) => {
            if (formatter != null) {
                const dataFormatter = formatter.getColumnTypeFormatter(columnType);
                if (dataFormatter != null) {
                    return dataFormatter.dhTimeZone;
                }
            }
            return undefined;
        });
        this.getValueTranslator = memoize((columnType, formatter) => {
            const timeZone = this.getTimeZone(columnType, formatter);
            return (value) => this.chartUtils.unwrapValue(value, timeZone);
        });
        this.widget = widget;
        this.refetch = refetch;
        this.chartUtils = new ChartUtils(dh);
        this.handleFigureUpdated = this.handleFigureUpdated.bind(this);
        this.handleWidgetUpdated = this.handleWidgetUpdated.bind(this);
        const widgetData = getWidgetData(widget);
        // Chart only fetches the model layout once on init, so it needs to be set
        // before the widget is subscribed to.
        this.updateLayout(widgetData);
        // The calendar is only fetched once at init.
        this.updateCalendar(widgetData);
        // The input filter columns are set once at init.
        this.updateFilterColumns(widgetData);
        this.setTitle(this.getDefaultTitle());
    }
    getData() {
        const hydratedData = [...this.plotlyData];
        this.tableColumnReplacementMap.forEach((columnReplacements, tableId) => {
            const tableData = this.tableDataMap.get(tableId);
            if (tableData == null) {
                throw new Error(`No tableData for table ID ${tableId}`);
            }
            // Replace placeholder arrays with actual data
            columnReplacements.forEach((paths, columnName) => {
                paths.forEach(destination => {
                    var _a, _b, _c;
                    // The JSON pointer starts w/ /plotly/data and we don't need that part
                    const parts = getPathParts(destination);
                    const single = isSingleValue(hydratedData, parts);
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    let selector = hydratedData;
                    for (let i = 0; i < parts.length; i += 1) {
                        if (i !== parts.length - 1) {
                            selector = selector[parts[i]];
                        }
                        else if (single) {
                            selector[parts[i]] = (_b = (_a = tableData[columnName]) === null || _a === void 0 ? void 0 : _a[0]) !== null && _b !== void 0 ? _b : null;
                        }
                        else {
                            selector[parts[i]] = (_c = tableData[columnName]) !== null && _c !== void 0 ? _c : [];
                        }
                    }
                });
            });
        });
        return hydratedData;
    }
    getLayout() {
        return this.layout;
    }
    close() {
        var _a;
        super.close();
        (_a = this.widget) === null || _a === void 0 ? void 0 : _a.close();
        this.widget = undefined;
    }
    async subscribe(callback) {
        var _a;
        if (this.isSubscribed) {
            log.debug('already subscribed');
            return;
        }
        log.debug('subscribing');
        super.subscribe(callback);
        if (this.widget == null) {
            this.widget = await this.refetch();
        }
        const widgetData = getWidgetData(this.widget);
        this.handleWidgetUpdated(widgetData, this.widget.exportedObjects);
        this.isSubscribed = true;
        this.widgetUnsubscribe = this.widget.addEventListener(this.dh.Widget.EVENT_MESSAGE, ({ detail }) => {
            this.handleWidgetUpdated(JSON.parse(detail.getDataAsString()), detail.exportedObjects);
        });
        this.tableReferenceMap.forEach((_, id) => this.subscribeTable(id));
        // If there are no tables to fetch data from, the chart is ready to render
        // Normally this event only fires once at least 1 table has fetched data
        // Without this, the chart shows an infinite loader if there are no tables
        if (this.tableColumnReplacementMap.size === 0) {
            this.fireUpdate(this.getData());
        }
        if (this.filterColumnMap != null) {
            // there are filters, so the server expects the filter to be sent
            this.sendFilterUpdated((_a = this.filterMap) !== null && _a !== void 0 ? _a : new Map());
        }
    }
    unsubscribe(callback) {
        var _a, _b;
        if (!this.isSubscribed) {
            return;
        }
        super.unsubscribe(callback);
        (_a = this.widgetUnsubscribe) === null || _a === void 0 ? void 0 : _a.call(this);
        this.isSubscribed = false;
        this.tableReferenceMap.forEach((_, id) => this.removeTable(id));
        (_b = this.widget) === null || _b === void 0 ? void 0 : _b.close();
        this.widget = undefined;
    }
    setRenderOptions(renderOptions) {
        var _a;
        this.handleWebGlAllowed(renderOptions.webgl, (_a = this.renderOptions) === null || _a === void 0 ? void 0 : _a.webgl);
        super.setRenderOptions(renderOptions);
    }
    /**
     * Handle the WebGL option being set in the render options.
     * If WebGL is enabled, traces have their original types as given.
     * If WebGL is disabled, replace traces that require WebGL with non-WebGL traces if possible.
     * Also, show a dismissible warning per-chart if there are WebGL traces that cannot be replaced.
     * @param webgl The new WebGL value. True if WebGL is enabled.
     * @param prevWebgl The previous WebGL value
     */
    handleWebGlAllowed(webgl = true, prevWebgl = true) {
        setWebGlTraceType(this.plotlyData, webgl && this.isWebGlSupported, this.webGlTraceIndices);
        const needsBlocker = hasUnreplaceableWebGlTraces(this.plotlyData);
        // If WebGL is disabled and there are traces that require WebGL, show a warning that is dismissible on a per-chart basis
        if (needsBlocker && !webgl && !this.hasAcknowledgedWebGlWarning) {
            this.fireBlocker([
                'WebGL is disabled but this chart cannot render without it. Check the Advanced section in the settings to enable WebGL or click below to render with WebGL for this chart.',
            ]);
        }
        else if (webgl && !prevWebgl && needsBlocker) {
            // clear the blocker but not the acknowledged flag in case WebGL is disabled again
            this.fireBlockerClear(false);
        }
    }
    fireBlockerClear(isAcknowledged = true) {
        super.fireBlockerClear();
        this.hasAcknowledgedWebGlWarning =
            isAcknowledged || this.hasAcknowledgedWebGlWarning;
    }
    updateLayout(data) {
        const { figure } = data;
        const { plotly } = figure;
        const { layout: plotlyLayout = {} } = plotly;
        // @deephaven/chart Chart component mutates the layout
        // If we want updates like the zoom range, we must only set the layout once on init
        // The title is currently the only thing that can be updated after init
        if (Object.keys(this.layout).length > 0) {
            return;
        }
        this.layout = Object.assign({}, plotlyLayout);
    }
    /**
     * Check if the timezone has changed in the new formatter
     * @param formatter The new formatter
     * @returns True if the timezone has changed
     */
    timeZoneChanged(formatter) {
        var _a, _b, _c;
        const timeZone = (_b = (_a = this.formatter) === null || _a === void 0 ? void 0 : _a.getColumnTypeFormatter('datetime')) === null || _b === void 0 ? void 0 : _b.dhTimeZone.id;
        const newTimeZone = (_c = formatter.getColumnTypeFormatter('datetime')) === null || _c === void 0 ? void 0 : _c.dhTimeZone.id;
        return timeZone !== newTimeZone && newTimeZone != null;
    }
    /**
     * Update the calendar object from the data
     * @param data The new data to update the calendar from
     */
    updateCalendar(data) {
        const { calendar } = data.figure.deephaven;
        if (calendar != null) {
            // Timezone must be replaced for accurate rangebreaks.
            const timeZone = this.dh.i18n.TimeZone.getTimeZone(calendar.timeZone);
            this.calendar = Object.assign(Object.assign({}, calendar), { timeZone, holidays: calendar.holidays.map((holiday, i) => {
                    const { date } = holiday;
                    // date is a really a string at this point, but it should be a LocalDate object
                    const dateObj = new Date(date);
                    const year = dateObj.getFullYear();
                    const month = dateObj.getMonth();
                    const day = dateObj.getDate();
                    return Object.assign(Object.assign({}, holiday), { date: {
                            valueOf: () => date,
                            getYear: () => year,
                            getMonthValue: () => month,
                            getDayOfMonth: () => day,
                            toString: () => date,
                        } });
                }) });
        }
    }
    /**
     * Fire an event to update the rangebreaks on the chart.
     * @param formatter The formatter to use to set the rangebreaks. If not provided, the current formatter is used.
     */
    fireRangebreaksUpdated(formatter = this.formatter) {
        if (!formatter) {
            return;
        }
        const layoutUpdate = setRangebreaksFromCalendar(formatter, this.calendar, this.layout, this.chartUtils);
        if (layoutUpdate) {
            this.fireLayoutUpdated(layoutUpdate);
        }
    }
    /**
     * Update the filter columns from the data.
  
     * @param data The new data to update the filter columns from
     */
    updateFilterColumns(data) {
        const { deephaven } = data.figure;
        const { filterColumns } = deephaven;
        if (filterColumns != null) {
            this.filterColumnMap = new Map(filterColumns.columns.map(({ name, type }) => [name, { name, type }]));
            // get all columns that have required = true
            this.requiredColumns = new Set(filterColumns.columns
                .filter(({ required }) => required)
                .map(({ name }) => name));
        }
    }
    /**
     * Unsubscribe from a table.
     * @param id The table ID to unsubscribe from
     */
    unsubscribeTable(id) {
        var _a;
        (_a = this.tableSubscriptionMap.get(id)) === null || _a === void 0 ? void 0 : _a.close();
        this.tableSubscriptionMap.delete(id);
    }
    /**
     * Fire an event to update the timezone on the chart data if it has changed.
     * @param formatter The new formatter
     */
    fireTimeZoneUpdated() {
        this.tableDataMap.forEach((_, tableId) => {
            const table = this.tableReferenceMap.get(tableId);
            if (table) {
                // resubscribe to get the data with the new timezone
                this.unsubscribeTable(tableId);
                this.subscribeTable(tableId);
            }
        });
        this.fireUpdate(this.getData());
    }
    setFormatter(formatter) {
        setDefaultValueFormat(this.plotlyData, this.defaultValueFormatSet, this.dataTypeMap, formatter);
        // Only update if isSubscribed because otherwise the events are unnecessary and buggy
        if (this.isSubscribed && this.timeZoneChanged(formatter)) {
            this.fireRangebreaksUpdated(formatter);
            this.fireTimeZoneUpdated();
        }
        super.setFormatter(formatter);
    }
    handleWidgetUpdated(data, references) {
        var _a, _b, _c, _d, _e, _f;
        log.debug('handleWidgetUpdated', data, references);
        const { figure, new_references: newReferences, removed_references: removedReferences, } = data;
        const { plotly, deephaven } = figure;
        const { layout: plotlyLayout = {} } = plotly;
        this.tableColumnReplacementMap = getDataMappings(data);
        this.plotlyData = plotly.data;
        if (!deephaven.is_user_set_template) {
            removeColorsFromData((_c = (_b = (_a = plotlyLayout === null || plotlyLayout === void 0 ? void 0 : plotlyLayout.template) === null || _a === void 0 ? void 0 : _a.layout) === null || _b === void 0 ? void 0 : _b.colorway) !== null && _c !== void 0 ? _c : [], this.plotlyData);
        }
        this.defaultValueFormatSet = replaceValueFormat(this.plotlyData);
        // Retrieve the indexes of traces that require WebGL so they can be replaced if WebGL is disabled
        this.webGlTraceIndices = getReplaceableWebGlTraceIndices(this.plotlyData);
        this.handleWebGlAllowed((_d = this.renderOptions) === null || _d === void 0 ? void 0 : _d.webgl);
        this.fireRangebreaksUpdated();
        newReferences.forEach(async (id, i) => {
            this.tableDataMap.set(id, {}); // Plot may render while tables are being fetched. Set this to avoid a render error
            const table = (await references[i].fetch());
            this.addTable(id, table).then(() => {
                // The data type map requires the table to be added to the reference map
                this.dataTypeMap = getDataTypeMap(deephaven, this.tableReferenceMap);
                setDefaultValueFormat(this.plotlyData, this.defaultValueFormatSet, this.dataTypeMap, this.formatter);
            });
        });
        removedReferences.forEach(id => this.removeTable(id));
        // title and legend title are the only things expected to be updated after init from the layout
        if (typeof plotlyLayout.title === 'object' &&
            plotlyLayout.title.text != null) {
            this.fireLayoutUpdated({ title: plotlyLayout.title });
        }
        if (((_f = (_e = plotlyLayout.legend) === null || _e === void 0 ? void 0 : _e.title) === null || _f === void 0 ? void 0 : _f.text) != null) {
            this.fireLayoutUpdated({
                legend: Object.assign({ title: Object.assign({ text: plotlyLayout.legend.title.text }, plotlyLayout.legend.title) }, plotlyLayout.legend),
            });
        }
        // If there are no tables to fetch data from, the chart is ready to render
        // Normally this event only fires once at least 1 table has fetched data
        // Without this, the chart shows an infinite loader if there are no tables
        if (this.tableColumnReplacementMap.size === 0) {
            this.fireUpdate(this.getData());
        }
    }
    handleFigureUpdated(event, tableId) {
        const chartData = this.chartDataMap.get(tableId);
        const tableData = this.tableDataMap.get(tableId);
        if (chartData == null) {
            log.warn('Unknown chartData for this event. Skipping update');
            return;
        }
        if (tableData == null) {
            log.warn('No tableData for this event. Skipping update');
            return;
        }
        const { detail: figureUpdateEvent } = event;
        chartData.update(figureUpdateEvent);
        figureUpdateEvent.columns.forEach(column => {
            const valueTranslator = this.getValueTranslator(column.type, this.formatter);
            const columnData = chartData.getColumn(column.name, valueTranslator, figureUpdateEvent);
            tableData[column.name] = columnData;
        });
        if (this.isPaused) {
            this.hasPendingUpdate = true;
            return;
        }
        this.fireUpdate(this.getData());
    }
    async addTable(id, table) {
        if (this.tableReferenceMap.has(id)) {
            return;
        }
        let tableToAdd = table;
        const downsampleInfo = this.getDownsampleInfo(id, table);
        const needsDownsample = table.size > PlotlyExpressChartModel.AUTO_DOWNSAMPLE_SIZE;
        const canDownsample = typeof downsampleInfo !== 'string';
        const canFetch = PlotlyExpressChartModel.canFetch(table);
        const shouldDownsample = needsDownsample && !this.isDownsamplingDisabled;
        if (!canDownsample) {
            if (!canFetch) {
                log.debug(`Table ${id} too big to fetch ${table.size} items`);
                this.fireDownsampleFail(`Too many items to plot: ${Number(table.size).toLocaleString()} items.`);
                return;
            }
            if (shouldDownsample) {
                this.fireDownsampleFail(downsampleInfo);
                return;
            }
        }
        if (canDownsample && needsDownsample) {
            this.downsampleMap.set(id, downsampleInfo);
            try {
                this.fireDownsampleStart(null);
                tableToAdd = await downsample(this.dh, downsampleInfo);
                this.fireDownsampleFinish(null);
            }
            catch (e) {
                this.fireDownsampleFail(e);
                return;
            }
        }
        this.tableReferenceMap.set(id, tableToAdd);
        this.tableDataMap.set(id, {});
        if (this.isSubscribed) {
            this.subscribeTable(id);
        }
    }
    async updateDownsampledTable(id) {
        var _a, _b;
        const oldDownsampleInfo = this.downsampleMap.get(id);
        if (oldDownsampleInfo == null) {
            log.error(`No table found for id ${id}`);
            return;
        }
        const downsampleInfo = this.getDownsampleInfo(id, oldDownsampleInfo.originalTable);
        if (typeof downsampleInfo === 'string') {
            this.fireDownsampleFail(downsampleInfo);
            return;
        }
        if (areSameAxisRange(downsampleInfo.range, oldDownsampleInfo.range) &&
            downsampleInfo.width === oldDownsampleInfo.width) {
            log.debug('Range and width are the same, skipping downsample');
            return;
        }
        log.debug('Updating downsampled table', downsampleInfo);
        this.fireDownsampleStart(null);
        (_a = this.subscriptionCleanupMap.get(id)) === null || _a === void 0 ? void 0 : _a();
        (_b = this.tableSubscriptionMap.get(id)) === null || _b === void 0 ? void 0 : _b.close();
        this.subscriptionCleanupMap.delete(id);
        this.tableSubscriptionMap.delete(id);
        this.tableReferenceMap.delete(id);
        this.addTable(id, oldDownsampleInfo.originalTable);
    }
    setDownsamplingDisabled(isDownsamplingDisabled) {
        this.isDownsamplingDisabled = isDownsamplingDisabled;
        if (isDownsamplingDisabled && this.widget != null) {
            const widgetData = getWidgetData(this.widget);
            this.handleWidgetUpdated(widgetData, this.widget.exportedObjects);
            this.fireDownsampleFinish(null);
        }
    }
    /**
     * Gets info on how to downsample a table for plotting.
     * @param tableId The tableId to get downsample info for
     * @param table The table to get downsample info for
     * @returns DownsampleInfo if table can be downsampled.
     *          A string of the reason if the table cannot be downsampled.
     *          Null if the table does not need downsampling.
     */
    getDownsampleInfo(tableId, table) {
        var _a, _b, _c;
        const downsampleFailMessage = `Plotting ${Number(table.size).toLocaleString()} items may be slow.\nAre you sure you want to continue?`;
        const replacementMap = this.tableColumnReplacementMap.get(tableId);
        if (!replacementMap) {
            return 'Nothing to downsample';
        }
        const areAllLines = [...replacementMap.values()]
            .flat()
            .map(path => getPathParts(path)[0])
            .every(seriesIndex => {
            const series = this.plotlyData[parseInt(seriesIndex, 10)];
            return series != null && isLineSeries(series);
        });
        if (!areAllLines) {
            log.debug('Cannot downsample non-line series');
            return downsampleFailMessage;
        }
        let xCol = '';
        let xAxis;
        const yCols = [];
        const replacementEntries = [...replacementMap.entries()];
        for (let i = 0; i < replacementEntries.length; i += 1) {
            const [columnName, paths] = replacementEntries[i];
            const pathParts = paths.map(getPathParts);
            for (let j = 0; j < pathParts.length; j += 1) {
                const [seriesIdx, xOrY] = pathParts[j];
                const series = this.plotlyData[parseInt(seriesIdx, 10)];
                if (xOrY === 'x') {
                    if (xCol !== '' && columnName !== xCol) {
                        log.debug('Cannot downsample multiple x columns');
                        return downsampleFailMessage;
                    }
                    xCol = columnName;
                    const axisName = `${series.xaxis[0]}axis${(_a = series.xaxis[1]) !== null && _a !== void 0 ? _a : ''}`;
                    xAxis = this.layout[axisName]; // The cast makes TS happy
                    if (xAxis != null && !isLinearAxis(xAxis) && !isAutoAxis(xAxis)) {
                        return 'Cannot downsample non-linear x axis';
                    }
                }
                else {
                    yCols.push(columnName);
                    const axisName = `${series.yaxis[0]}axis${(_b = series.yaxis[1]) !== null && _b !== void 0 ? _b : ''}`;
                    const yAxis = this.layout[axisName]; // The cast makes TS happy
                    if (yAxis != null && !isLinearAxis(yAxis) && !isAutoAxis(yAxis)) {
                        return 'Cannot downsample non-linear y axis';
                    }
                }
            }
        }
        if (xAxis == null) {
            return 'Cannot downsample without an x axis';
        }
        // Copy the range in case plotly mutates it
        const range = xAxis.autorange === false ? [...((_c = xAxis.range) !== null && _c !== void 0 ? _c : [])] : null;
        return {
            type: 'linear',
            originalTable: table,
            xCol,
            yCols,
            width: this.getPlotWidth(),
            range,
            rangeType: xAxis.type === 'date' ? 'date' : 'number',
        };
    }
    subscribeTable(id) {
        const table = this.tableReferenceMap.get(id);
        const columnReplacements = this.tableColumnReplacementMap.get(id);
        if (table != null &&
            columnReplacements != null &&
            columnReplacements.size > 0 &&
            !this.tableSubscriptionMap.has(id)) {
            this.chartDataMap.set(id, new this.dh.plot.ChartData(table));
            const columnNames = new Set(columnReplacements.keys());
            const columns = table.columns.filter(({ name }) => columnNames.has(name));
            const subscription = table.subscribe(columns);
            this.tableSubscriptionMap.set(id, subscription);
            this.subscriptionCleanupMap.set(id, subscription.addEventListener(this.dh.Table.EVENT_UPDATED, e => this.handleFigureUpdated(e, id)));
        }
    }
    removeTable(id) {
        var _a, _b;
        (_a = this.subscriptionCleanupMap.get(id)) === null || _a === void 0 ? void 0 : _a();
        (_b = this.tableSubscriptionMap.get(id)) === null || _b === void 0 ? void 0 : _b.close();
        this.tableReferenceMap.delete(id);
        this.downsampleMap.delete(id);
        this.subscriptionCleanupMap.delete(id);
        this.tableSubscriptionMap.delete(id);
        this.chartDataMap.delete(id);
        this.tableDataMap.delete(id);
        this.tableColumnReplacementMap.delete(id);
    }
    fireUpdate(data) {
        super.fireUpdate(data);
        this.hasPendingUpdate = false;
        // TODO: This will fire on first call to `fireUpdate` even though other data
        // may still be loading. We should consider making this smarter to fire after
        // all initial data has loaded.
        // https://github.com/deephaven/deephaven-plugins/issues/267
        // If not subscribed, the fireLoadFinished will not go through since there is no listeners
        // which results in a loading spinner that does not go away on its own
        // isSubscribed can also be checked before calling fireUpdate, but this is a
        // subtle bug that is good to check for here just in case
        if (!this.hasInitialLoadCompleted && this.isSubscribed) {
            this.fireLoadFinished();
            this.hasInitialLoadCompleted = true;
        }
    }
    setDimensions(rect) {
        super.setDimensions(rect);
        ChartUtils.getLayoutRanges(this.layout);
        this.downsampleMap.forEach((_, id) => {
            this.updateDownsampledTable(id);
        });
    }
    getFilterColumnMap() {
        return this.filterColumnMap;
    }
    isFilterRequired() {
        // if any of the required columns are not in the filter map, then filters are still required
        return Array.from(this.requiredColumns).some(column => !this.filterMap || !this.filterMap.has(column));
    }
    setFilter(filterMap) {
        super.setFilter(filterMap);
        this.filterMap = filterMap;
        if (this.isSubscribed) {
            this.sendFilterUpdated(filterMap);
        }
    }
    /**
     * Fire an event to update the filters on the chart.
     * @param filterMap The filter map to send to the server
     */
    sendFilterUpdated(filterMap) {
        var _a;
        // Only send the filter update if filters are not required and the filter columns are set
        // They will either be set or none are required
        if (!this.isFilterRequired() && this.filterColumnMap.size > 0) {
            (_a = this.widget) === null || _a === void 0 ? void 0 : _a.sendMessage(JSON.stringify({
                type: 'FILTER',
                filterMap: Object.fromEntries(filterMap),
            }));
        }
    }
    pauseUpdates() {
        this.isPaused = true;
    }
    resumeUpdates() {
        this.isPaused = false;
        if (this.hasPendingUpdate) {
            this.fireUpdate(this.getData());
        }
    }
    shouldPauseOnUserInteraction() {
        return (this.hasScene() || this.hasGeo() || this.hasMapbox() || this.hasPolar());
    }
    hasScene() {
        return this.plotlyData.some(d => 'scene' in d && d.scene != null);
    }
    hasGeo() {
        return this.plotlyData.some(d => 'geo' in d && d.geo != null);
    }
    hasMapbox() {
        return this.plotlyData.some(({ type }) => type === null || type === void 0 ? void 0 : type.includes('mapbox'));
    }
    hasPolar() {
        return this.plotlyData.some(({ type }) => type === null || type === void 0 ? void 0 : type.includes('polar'));
    }
    getPlotWidth() {
        var _a, _b, _c, _d;
        if (!this.rect || !this.rect.width) {
            return 0;
        }
        return Math.max(this.rect.width -
            ((_b = (_a = this.layout.margin) === null || _a === void 0 ? void 0 : _a.l) !== null && _b !== void 0 ? _b : 0) -
            ((_d = (_c = this.layout.margin) === null || _c === void 0 ? void 0 : _c.r) !== null && _d !== void 0 ? _d : 0), 0);
    }
    getPlotHeight() {
        var _a, _b, _c, _d;
        if (!this.rect || !this.rect.height) {
            return 0;
        }
        return Math.max(this.rect.height -
            ((_b = (_a = this.layout.margin) === null || _a === void 0 ? void 0 : _a.t) !== null && _b !== void 0 ? _b : 0) -
            ((_d = (_c = this.layout.margin) === null || _c === void 0 ? void 0 : _c.b) !== null && _d !== void 0 ? _d : 0), 0);
    }
}
/**
 * The size at which the chart will automatically downsample the data if it can be downsampled.
 * If it cannot be downsampled, but the size is below MAX_FETCH_SIZE,
 * the chart will show a confirmation to fetch the data since it might be a slow operation.
 */
PlotlyExpressChartModel.AUTO_DOWNSAMPLE_SIZE = 30000;
/**
 * The maximum number of items that can be fetched from a table.
 * If a table is larger than this, the chart will not be fetched.
 * This is to prevent the chart from fetching too much data and crashing the browser.
 */
PlotlyExpressChartModel.MAX_FETCH_SIZE = 1000000;
export default PlotlyExpressChartModel;
//# sourceMappingURL=PlotlyExpressChartModel.js.map