import * as t from "./types";
import * as constants from './constants';
import { RegisterImportPool, DynDep, ImportPool } from "./Base";
import { Lino } from "./preprocessors";

const exModulePromises: ImportPool = {
    // @ts-ignore
    queryString: import(/* webpackChunkName: "queryString_ActionHandler" */"query-string"),
    // @ts-ignore
    weakKey: import(/* webpackChunkName: "weakKey_ActionHandler" */"weak-key"),
    // @ts-ignore
    _: import(/* webpackChunkName: "lodash_ActionHandler" */"lodash"),
    // @ts-ignore
    whatwgFetch: import(/* webpackChunkName: "whatwg_fetch_ActionHandler" */"whatwg-fetch"),
    // @ts-ignore
    AbortController: import(/* webpackChunkName: "abort_controller_ActionHandler" */"abort-controller"),
    // @ts-ignore
    u: import(/* webpackChunkName: "LinoUtils_ActionHandler" */"./LinoUtils"),
    // @ts-ignore
    i18n: import(/* webpackChunkName: "i18n_ActionHandler" */"./i18n")
};RegisterImportPool(exModulePromises);


export class URLParser extends DynDep implements t.URLParser {
    static requiredModules: string[] = ["queryString", "u"]
    static iPool: ImportPool = exModulePromises;
    queryString: any;
    async prepare() {
        await super.prepare();
        this.queryString = this.ex.queryString.default;
    }
    onReady({next}: t.ParamsDynDep) {next(this)}

    parseShallow = (s: string, {sanitizeValue=true} = {}): t.ObjectAny => {
        if (s.startsWith("?")) s = s.slice(1);
        const object = this.queryString.parse(s);
        if (sanitizeValue) Object.keys(object).forEach(
            key => object[key] = this.sanitize(object[key]));
        return object;
    }

    parse = (s: string, {sanitizeValue=true} = {}): t.ObjectAny => {
        if (s.startsWith("?")) s = s.slice(1);
        let object = this.queryString.parse(s);
        Object.keys(object).forEach(element => {
            object[element] = this.sanitizeParse(object[element], sanitizeValue);
        });
        return object;
    }

    sanitize = (v: any): any => {
        let v_;
        if (typeof v === 'string') {
            let match = v.match(constants.DATE_EXP);
            if (match !== null) return v;
            match = v.match(constants.TIME_EXP);
            if (match !== null) return v;
            v_ = parseFloat(v);
            if (!this.ex.u.isNaN(v_)) return v_;
            v_ = v.toLowerCase();
            if (v_ === "true") return true;
            if (v_ === "false") return false;
        }
        return v;
    }

    sanitizeArrayUnparse = (array: any[]): any[] => {
        array.forEach(
            (element, i) => (array[i] = this.sanitizeUnparse(element)));
        return array;
    }

    sanitizeMapUnparse = (map: Map<any, any>): t.ObjectAny => {
        let object: t.ObjectAny = this.sanitizeObjectUnparse(Object.fromEntries(map));
        object.keyOrder = Array.from(map.keys());
        return object;
    }

    sanitizeObjectUnparse = (object: t.ObjectAny): t.ObjectAny => {
        Object.keys(object).forEach(
            key => (object[key] = this.sanitizeUnparse(object[key])));
        return object;
    }

    sanitizeParse = (v: any, sanitizeValue: boolean): any => {
        if (typeof v === "string" && v.startsWith(constants.STR_JSON_ITENT)) {
            v = JSON.parse(v.split(constants.STR_JSON_ITENT)[1]);
            sanitizeValue = false;
        }
        if (Array.isArray(v)) v.forEach(
            (item, i) => (v[i] = this.sanitizeParse(item, sanitizeValue)))
        else if (v instanceof Object) {
            Object.keys(v).forEach(key => v[key] = this.sanitizeParse(v[key], sanitizeValue));
            if (v.hasOwnProperty("keyOrder")) {
                let m = new Map();
                v.keyOrder.forEach(key => m.set(key, v[key]));
                v = m;
            }
        } else if (sanitizeValue) v = this.sanitize(v);
        return v;
    }

    sanitizeUnparse = (element: any): any => {
        if (element instanceof Map) return this.sanitizeMapUnparse(element)
        else if (Array.isArray(element)) return this.sanitizeArrayUnparse(element)
        else if (element instanceof Object) return this.sanitizeObjectUnparse(element)
        else return element;
    }

    stringify = (object: t.ObjectAny, usePrefix: boolean = false): string => {
        return this.queryString.stringify(
            this.stringifyNONPrimitives(this.sanitizeObjectUnparse(object), usePrefix));
    }

    stringifyNONPrimitives = (
        thing: t.ObjectAny, usePrefix: boolean = true
    ): t.ObjectAny => {
        Object.keys(thing).forEach(key => {
            let v = thing[key];
            if (key === constants.URL_PARAM_GRIDFILTER) thing[key] = (
                usePrefix ? constants.STR_JSON_ITENT : "") + JSON.stringify(v)
            else if (Array.isArray(v)) {
                v.forEach((item, i) => {
                    if (item instanceof Object) v[i] = (
                        usePrefix ? constants.STR_JSON_ITENT : "") + JSON.stringify(item)
                })
            }
            else if (v instanceof Object) thing[key] = (
                usePrefix ? constants.STR_JSON_ITENT : "") + JSON.stringify(v);
        });
        return thing;
    }
}

export interface ActionHandler extends t.ActionHandler {};

export class ActionHandler extends DynDep implements ActionHandler {
    static requiredModules: string[] = ["u", "weakKey", "_", "whatwgFetch",
        "AbortController", "queryString", "i18n"];
    static iPool: ImportPool = exModulePromises;
    async prepare(): Promise<void> {
        this.ex.weakKey = this.ex.weakKey.default;
        this.ex._ = this.ex._.default;
        this.ex.i18n = this.ex.i18n.default;
        this.ex.AbortController = this.ex.AbortController.default;
        this.ex.fetchPolyfill = this.ex.whatwgFetch.fetch;
        this.abortController = new this.ex.AbortController();
    };
    onReady({context, next}: t.ParamsDynDep) {
        this.context = context;

        this.refName = this.ex.weakKey(this);
        context.APP.rps[this.refName] = this;

        this.reloadables = {};

        this.cloneState = this.cloneState.bind(this);
        this.clearMod = this.clearMod.bind(this);
        this.copyData = this.copyData.bind(this);
        this.defaultParams = this.defaultParams.bind(this);
        this.defaultStaticParams = this.defaultStaticParams.bind(this);
        this.discardModDConfirm = this.discardModDConfirm.bind(this);
        this.executeAction = this.executeAction.bind(this);
        this.fetch = this.fetch.bind(this);
        this.getAction = this.getAction.bind(this);
        this.getCallback = this.getCallback.bind(this);
        this.getParams = this.getParams.bind(this);
        this.getPath = this.getPath.bind(this);
        this.handledFetch = this.handledFetch.bind(this);
        this.handleActionResponse = this.handleActionResponse.bind(this);
        this.handleAjaxResponse = this.handleAjaxResponse.bind(this);
        this.load = this.load.bind(this);
        this.multiRowParams = this.multiRowParams.bind(this);
        this.refresh = this.refresh.bind(this);
        this.reload = this.reload.bind(this);
        this.silentFetch = this.silentFetch.bind(this);
        this.submit = this.submit.bind(this);
        this.submitDetailCallback = this.submitDetailCallback.bind(this);
        this.submitFiles = this.submitFiles.bind(this);
        this.update = this.update.bind(this);

        this.parser = new URLParser({next: () => next(this)});
    }

    clearMod = () => {
        this.context.dataContext.clearMod();
        for (const variable of Object.values(this.context.children)) {
            let dataContext = (variable as t.NavigationContext).dataContext;
            if (dataContext) dataContext.clearMod();
        }
    }

    clearRequestPool = () => {
        this.abortController.abort();
        this.abortController = new this.ex.AbortController();
    }

    cloneState = ({flags = (constants.FLAG_CLONE_URL | constants.FLAG_CLONE_UI |
        constants.FLAG_CLONE_DATA), recursive = false}: {
            flags?: number, recursive?: boolean} = {}
    ): t.StateClone => {
        let clone: t.StateClone = {clone: true};
        if (flags & constants.FLAG_CLONE_DATA) this.copyData(clone);
        if (flags & constants.FLAG_CLONE_UI)
            this.getUIConfigParams(Object.assign(clone, {params: {}}).params);
        if (flags & constants.FLAG_CLONE_URL) {
            if (!(flags & constants.FLAG_CLONE_UI))
                Object.assign(clone, {params: {}});
            Object.assign(clone, {windowGlobals: {}});
            this.getBasics(clone.params);
            this.getParams(clone);
        }
        if (recursive) {
            const children = Object.values(this.context.children)
            if (children.length)
                clone.children = children.map((c: t.NavigationContext) => ({
                    [c.static.actorData.id]: c.actionHandler
                        .cloneState({flags, recursive})}));
        }
        return clone;
    }

    copyContext = (where: t.NavigationContext, params: t.ViewParams = {}) => {
        const clone: t.StateClone = this.cloneState({
            flags: constants.FLAG_CLONE_UI | constants.FLAG_CLONE_URL});
        Object.assign(clone.params, params);
        where.history.pushPath({
            pathname: clone.params.path, params: clone.params});
    }

    copyData = (clone: t.StateClone): t.StateClone => {
        clone.mutableData = {...this.context.dataContext.mutableContext};
        clone.immutableData = {...this.context.dataContext.contextBackup};
        return clone;
    }

    URLAppendPKFromSR = (uri: string, sr: (number | string)[]) => {
        const pk = (this.context.filled(sr) && sr.length) ? sr[0] : null;
        if (this.context.filled(pk)) uri += `/${pk}`;
        return uri;
    }

    executeAction = async ({action, actorId, status, preprocessedStack,
        response_callback, rowIndex, pollContext
    }: t.ArgsExecute) => {
        delete preprocessedStack.callback;
        let queryParams = preprocessedStack as t.DataParams;
        if (action.http_method === "GET")
            queryParams[constants.URL_PARAM_FORMAT] = constants.URL_FORMAT_JSON;

        const ad = await this.context.getActorData(actorId);

        let url = `api/${actorId.split(".").join("/")}`;
        if (action.full_name !== ad.delete_action)
            url = this.URLAppendPKFromSR(url, queryParams[constants.URL_PARAM_SELECTED]);

        const makeCall = (p) => {
            if (action.http_method === "GET") this.handledFetch({
                path: `${url}?${this.parser.stringify(p)}`,
                response_callback: response_callback})
            else {
                if (this.hasFiles()) this.submitFiles(p)
                else this.XHRPutPost({path: url, body: p,
                    response_callback: response_callback}, action.http_method);
            }
        }

        if (status && status.rqdata && status.xcallback) {
            status.rqdata["xcallback__" + status.xcallback.xcallback_id] = status.xcallback.choice;
            makeCall(status.rqdata);
            return
        }

        let dataParams: t.DataParams = Object.assign(
            this.mustHaveParams(), this.getModifiedData(rowIndex));

        const commonActor = (this.context.value.hasActor && actorId === this.context.static.actorData.id);

        if (commonActor) Object.assign(dataParams, this.commonParams());
        if (pollContext || commonActor) Object.assign(dataParams, this.getParams());
        Object.assign(dataParams, queryParams);

        if (status && this.context.filled(status.fv) && !action.window_action)
            Object.assign(dataParams, {fv: status.fv});

        makeCall(dataParams);
    }

    getHolders = (queryParams: t.QueryParams | t.StateClone): {viewHolder: t.QPView,
        windowHolder: t.QPWindowGlobals
    } => {
        let viewHolder: t.QPView, windowHolder: t.QPWindowGlobals;
        if ((queryParams as t.StateClone).clone) {
            viewHolder = (queryParams as t.StateClone).params;
            windowHolder = (queryParams as t.StateClone).windowGlobals;
        } else {
            viewHolder = (queryParams as t.QueryParams);
            windowHolder = (queryParams as t.QueryParams);
        }
        return {viewHolder, windowHolder};
    }

    defaultStaticParams = (queryParams: t.QueryParams = {}): t.QueryParams => {
        queryParams[constants.URL_PARAM_MASTER_PK] = this.context.value[
            constants.URL_PARAM_MASTER_PK];
        queryParams[constants.URL_PARAM_MASTER_TYPE] = this.context.value[
            constants.URL_PARAM_MASTER_TYPE];
        queryParams[constants.URL_PARAM_LINO_VERSION] = window.Lino[
            constants.URL_PARAM_LINO_VERSION];
        queryParams[constants.URL_PARAM_REQUESTING_PANEL] = this.refName;
        return queryParams;
    }

    mustHaveParams = (
        holder: t.QueryParams | t.StateClone = {}
    ): t.QueryParams | t.StateClone => {
        holder[constants.URL_PARAM_SUBST_USER] = this.context.value[
            constants.URL_PARAM_SUBST_USER];
        holder[constants.URL_PARAM_USER_LANGUAGE] = this.context.value[
            constants.URL_PARAM_USER_LANGUAGE];
        return holder;
    }

    commonParams = (
        queryParams: t.QueryParams | t.StateClone = {}
    ): t.QueryParams | t.StateClone => {
        const {viewHolder, windowHolder} = this.getHolders(queryParams);
        this.mustHaveParams(windowHolder);
        viewHolder[constants.URL_PARAM_WINDOW_TYPE] = this.context.value[
            constants.URL_PARAM_WINDOW_TYPE];
        viewHolder[constants.URL_PARAM_DISPLAY_MODE] = this.context.value[
            constants.URL_PARAM_DISPLAY_MODE];
        this.defaultStaticParams(viewHolder);
        return queryParams;
    }

    defaultParams = (
        queryParams: t.QueryParams | t.StateClone = ({} as t.QueryParams)
    ): t.QueryParams | t.StateClone => {
        const {viewHolder, windowHolder} = this.getHolders(queryParams);

        this.commonParams(queryParams);

        if (this.context.static.actorData &&
            this.context.static.actorData.use_detail_params_value)
            viewHolder[constants.URL_PARAM_PARAM_VALUES] = this.context.APP
                .URLContext.value[constants.URL_PARAM_PARAM_VALUES]
        else viewHolder[constants.URL_PARAM_PARAM_VALUES] = this.context.value[
            constants.URL_PARAM_PARAM_VALUES]

        // this.defaultStaticParams(viewHolder);
        viewHolder[constants.URL_PARAM_FILTER] = this.context.value[
            constants.URL_PARAM_FILTER];
        return queryParams;
    }

    masterRelateForSlave = () => {
        const { context } = this;
        return {
            [constants.URL_PARAM_MASTER_PK]: constants.ABSTRACT_PRIMARY_KEYS
                .includes(context.value.pk)
                ? context.dataContext.mutableContext.id
                : context.value.pk,
            [constants.URL_PARAM_MASTER_TYPE]: context.static.actorData.content_type
        }
    }

    discardModDConfirm = (
        {agree = (e: any) => {}, disagree = (e: any) => {}}
    ): void => {
        let dF = this.context.APP.dialogFactory, id = this.context.newSlug().toString();
        dF.createCallback({
            actionHandler: this, agree: e => {
                this.clearMod();
                agree(e);
                dF.removeCallback(id);
            },
            disagree: e => {disagree(e);dF.removeCallback(id);}, factory: dF,
            id: id, simple: true, title: this.ex.i18n.t("Confirmation"),
            message: this.ex.i18n.t("Discard changes to current record?")});
    }

    multiRowParams = (queryParams: t.QueryParams): t.QueryParams => {
        queryParams[constants.URL_PARAM_START] = this.context.value[
            constants.URL_PARAM_START];
        queryParams[constants.URL_PARAM_LIMIT] = this.context.value[
            constants.URL_PARAM_LIMIT];
        queryParams[constants.URL_PARAM_SORT] = this.context.value[
            constants.URL_PARAM_SORT];
        queryParams[constants.URL_PARAM_SORTDIR] = this.context.value[
            constants.URL_PARAM_SORTDIR];
        let fts = this.context.value[constants.URL_PARAM_GRIDFILTER];
        if (fts.length) queryParams[constants.URL_PARAM_GRIDFILTER] = fts;
        return queryParams;
    }

    getAction = (
        action_full_name: string, preprocess: boolean = true
    ): {action: t.Action, preprocessedStack: t.PreprocessedStack} => {
        const action: t.Action = this.context.APP.state.site_data.action_definitions[action_full_name];
        const preprocessedStack: t.PreprocessedStack = {
            [constants.URL_PARAM_ACTION_NAME]: action[constants.URL_PARAM_ACTION_NAME]};
        if (preprocess) this.preprocess(action.preprocessor, preprocessedStack);
        return {action: action, preprocessedStack: preprocessedStack}
    }

    getCallback = (action_name: string): t.ResponseCallback => {
        if (action_name === 'submit_detail') return this.submitDetailCallback;
        if (action_name === 'sign_in') return (data) => {
            data[constants.URL_PARAM_ACTION_NAME] = action_name;
            // console.log("sign_in callback data", data)
        }
        return (data) => {};
    }

    getDefaultContextPath = (): t.ContextPath => {
        let ctx = this.context.value;
        return {
            pathname: ctx.actorId === 'Dashboard'
                ? "api/system/Dashboard" : ctx.path.slice(1),
            params: {
                [constants.URL_PARAM_FORMAT]: constants.URL_FORMAT_JSON
            }
        }
    }

    getGridFilters = (): t.GridFilter[] => {
        return Array.from(this.context.value.gridFilters.values()).filter(
            (ft: t.GridFilter) => {
                return this.context.filled(ft.value)}) as t.GridFilter[];
    }

    getModifiedData = (rowIndex?: number | 'detail'): t.Data => {
        let data: t.Data = {};
        if (!this.context.dataContext) return data;

        if (this.context.contextType === constants.CONTEXT_TYPE_ACTION) {
            data = {...this.context.dataContext.mutableContext.data};
            delete data.disabled_fields;
            delete data.disable_editing;
        } else if ([undefined, constants.DISPLAY_MODE_DETAIL as "detail"].includes(rowIndex as "detail")) {
            let mutableContextData = this.context.dataContext.mutableContext.data;
            this.context.dataContext.mutableContext.modified.forEach(name => {
                data[name] = mutableContextData[name];
                if (!this.context.filled(data[name])) data[name] = "";
                if (mutableContextData.hasOwnProperty(name + "Hidden"))
                    data[name + "Hidden"] = mutableContextData[name + "Hidden"];
            });
        } else {
            let cols = this.context.static.actorData.col,
                rowData = this.context.dataContext.mutableContext.rows[rowIndex];
            this.context.dataContext.mutableContext.modifiedRows[rowIndex]
            .forEach((fields_index, i) => {
                let name = this.context.value.showableColumns.get(fields_index),
                    fih = cols.find(col => col.fields_index === fields_index)
                        .fields_index_hidden;
                if (this.context.filled(fih)) data[name + "Hidden"] = rowData[fih];
                data[name] = rowData[fields_index];
            });
        }
        return data;
    }

    getBasics = (holder: t.ContextBasics): t.ContextBasics => {
        holder.path = this.context.value.path;
        holder.hasActor = this.context.value.hasActor;
        return holder;
    }

    getParams = (
        queryParams: t.QueryParams | t.StateClone = ({} as t.QueryParams)
    ): t.QueryParams | t.StateClone => {
        queryParams = this.defaultParams(queryParams) as t.QueryParams;
        if (constants.DISPLAY_MODE_DETAIL !== this.context.value[constants.URL_PARAM_DISPLAY_MODE]) {
            return this.multiRowParams((queryParams as t.StateClone).clone ? (queryParams as t.StateClone).params: (queryParams as t.QueryParams));
        }
        return queryParams;
    }

    getPath = (pathinfo?: t.ContextPath): string => {
        if (pathinfo === undefined) pathinfo = this.getDefaultContextPath();
        // let queryParams: t.QueryParams = this.getParams();
        let queryParams = (this.getParams() as t.QueryParams);
        Object.assign(queryParams, pathinfo.params);
        return `${pathinfo.pathname}?${this.parser.stringify(queryParams)}`;
    }

    getUIConfigParams = (params: t.UIConfigParams = {}): t.UIConfigParams => {
        params.editing_mode = this.context.value.editing_mode;
        params.pvPVisible = this.context.value.pvPVisible;
        params.showableColumns = this.context.value.showableColumns;
        params.sortField = this.context.value.sortField;
        params.sortOrder = this.context.value.sortOrder;
        params.tab = this.context.value.tab;
        params.toolbarState = this.context.value.toolbarState;
        return params;
    }

    reload = (): void => this.refresh(true);

    refresh = (reload: boolean = false): void => {
        this.context.dataContext.root.controller.abort();
        this.context.dataContext.root.controller = new this.ex.AbortController();

        // WINDOW_TYPE_TEXT is unique to a TextField & DISPLAY_MODE_DETAIL is
        // unique to SingleRow.
        this.context.setContextType(this.context.filled(this.context.value.fieldName)
            ? constants.CONTEXT_TYPE_TEXT_FIELD : this.context.value[
            constants.URL_PARAM_DISPLAY_MODE] === constants.DISPLAY_MODE_DETAIL
            ? constants.CONTEXT_TYPE_SINGLE_ROW : constants.CONTEXT_TYPE_MULTI_ROW);

        this.handledFetch({path: this.getPath(),
            signal: this.context.dataContext.root.controller.signal,
            response_callback: (data) => {
                if (data === null) return;
                if ([constants.CONTEXT_TYPE_SINGLE_ROW,
                    constants.CONTEXT_TYPE_TEXT_FIELD
                ].includes(this.context.contextType)) {
                    if (!data.hasOwnProperty('success')) data.success = true;
                }
                this.context.dataContext.set(data, false, {loading: false},
                    (mutableData) => {
                        const { context } = this;
                        if (context.contextType === constants.CONTEXT_TYPE_SINGLE_ROW) {
                            context.history.replace({[constants.URL_PARAM_SELECTED]: [mutableData.id]});
                        } else if (context.contextType === constants.CONTEXT_TYPE_MULTI_ROW) {
                            let pki = context.static.actorData.pk_index,
                                sr = [];
                            mutableData.rows.forEach(row => {
                                if (context.value[constants.URL_PARAM_SELECTED].includes(row[pki]))
                                    sr.push(row[pki]);
                            });
                            context.history.replace({[constants.URL_PARAM_SELECTED]: sr});
                        }
                        if (reload) {
                            const { toolbar } = context.dataContext.root;
                            if (toolbar) toolbar.setState({key: context.newSlug()});
                        }
                    }
                )}}, () => {
                    if (reload) this.context.dataContext.root.setState({
                        displayMode: null, loading: true});
                    else
                        this.context.dataContext.root.setState({loading: true});
                    });
    }

    refreshDelayedValue = (actorID: string | true): void => {
        let sLs = this.context.dataContext.refStore.slaveLeaves;
        if (actorID === true) Object.values(sLs).forEach(
            leaf => (leaf as {update: () => null}).update())
        else sLs[actorID] && sLs[actorID].update();
    }

    fetch = async ({path, signal, silent = false}: t.ArgsFetchXHR
    ): Promise<any> => {
        if (!silent) this.context.APP.setLoadMask();
        return await this.ex.fetchPolyfill(path, {signal: signal})
            .then(this.handleAjaxResponse).catch(() => null);
    }

    silentFetch = async ({path, signal}: t.ArgsFetchXHR): Promise<any> => {
        return await this.fetch({path: path, signal: signal, silent: true});
    }

    handledFetch = async (
        {path, signal, silent = false, response_callback}: t.ArgsFetchXHR,
    preFetch = () => {}): Promise<void> => {
        const doFetch = () => {
            preFetch();
            this.fetch({path: path, signal: signal, silent: silent}).then(
                async (data) => {
                    await this.handleActionResponse({
                        response: data, response_callback: response_callback})}
            );
        }
        if (silent || this.context.contextType === constants.CONTEXT_TYPE_ACTION
            || !this.context.isModified()
        ) {doFetch()} else {
            this.discardModDConfirm({agree: doFetch});
        }
    }

    handleActionResponse = async (
        {response, response_callback} : t.ArgsActionResponse
    ): Promise<void> => {
        if (response.version_mismatch) {
            this.context.APP.reload();
            return}
        let aH = this;
        if (response.info_message) console.log(response.info_message);
        if (response.debug_message) console.log(response.debug_message);
        if (response.warning_message) console.warn(response.warning_message);

        if (response_callback) response_callback(response);

        if (response.xcallback) { // confirmation dialogs
            let {id, title} = response.xcallback;
            aH.context.APP.dialogFactory.createCallback({
                id: id, message: response.message, title: title,
                xcallback: response.xcallback, actionHandler: aH});
            return;
        }

        if (response.close_window) {
            let otherAh = aH.context.parent.actionHandler;
            aH.context.void = true;
            if (aH.context.value[constants.URL_PARAM_ACTION_NAME] === aH.context.static.actorData.insert_action
                && otherAh.context.static.actorData
                && aH.context.static.actorData.id !== otherAh.context.static.actorData.id)
                otherAh.refreshDelayedValue(aH.context.static.actorData.id);
            aH.context.dataContext.root.forceClose();
            aH = otherAh;
        }

        if (response.eval_js) {
            eval(response.eval_js);
        }

        if (response.record_deleted && response.success) {
            aH.context.APP.toast.show({
                severity: "success",
                summary: this.ex.i18n.t("Success"),
                detail: response.message || this.ex.i18n.t("Record Deleted"),
            });
            if (aH.context.contextType === constants.CONTEXT_TYPE_SINGLE_ROW)
                aH.context.APP.navigate(-1);
            else if (aH.context.contextType === constants.CONTEXT_TYPE_MULTI_ROW) {
                await aH.context.history.replace({[constants.URL_PARAM_SELECTED]: []});
                aH.refresh();
            }
            return;
        }

        if (response.success && response.goto_url === "/" && response.close_window) {
            aH.context.APP.reset(response[constants.URL_PARAM_ACTION_NAME] === 'sign_in');
            return;
        }

        if (response.goto_url) {
            let url = response.goto_url;
            if (response.goto_url.includes('#')) {
                url = url.split("#")[1];
            }
            let [path, search] = url.split("?");
            if (search === undefined) search = "";
            aH.context.history.pushPath({
                pathname: path, params: aH.parser.parseShallow(search)});
        }

        if (response.open_url) {
            window.open(response.open_url);
        }

        if (response.message) {
            aH.context.APP.toast.show({
                severity: response.alert ? response.alert.toLowerCase() : response.success ? "success" : "info",
                summary: response.alert || (response.success ?
                    this.ex.i18n.t("Success") : this.ex.i18n.t("Info")),
                detail: response.message
            });
            if (aH.context.APP.data.user_state_change) {
                delete aH.context.APP.data.user_state_change;
                aH.context.APP.reset();
            }
        }

        if (response.clear_site_cache) {
            this.context.APP.reload();
            return;
        }

        if (response.refresh || response.refresh_all) {
            if (aH.context.APP.dashboard) aH.context.APP.dashboard.reloadData()
            else aH.reload();
            Object.values(aH.context.APP.URLContext.actionHandler.reloadables)
            .forEach((element:t.Reloadable) => element.reload());
        }
        if (response.refresh_delayed_value || response.refresh_all) {
            this.refreshDelayedValue(response.refresh_delayed_value);
        }
        if (response.hasOwnProperty("editing_mode")) {
            aH.context.history.replaceState({editing_mode: response.editing_mode});
        }
    }

    handleAjaxResponse = (resp: any): t.Data => {
        // TODO: Check for all status code:
        // https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
        this.context.APP.unsetLoadMask();
        let s = resp.status;
        if (s < 200) {
            this.context.APP.toast.show({
                severity: "warn",
                summary: this.ex.i18n.t("Unknown response"),
                detail: this.ex.i18n.t("See for status$t(colonSpaced){{statusCode}}",
                    {statusCode: s})
            });
            return {}
        } else
        if (s < 400) {return resp.json()} else
        if (s < 500) {
            resp.text().then((text) => {this.context.APP.toast.show(
                {severity: "error",
                    summary: this.ex.i18n.t("Bad Request"), detail: text})});

            if (resp.headers.map['content-type'].startsWith("application/json")) {
                return resp.json()
            } else return {success: false};
        } else {
            this.context.APP.setServerError();
            return {success: false};
        }
    }

    hasFiles = (): boolean => {
        return this.context.dataContext.mutableContext.UploadHandlerEvent !== null;
    }

    load = (): void => this.refresh();

    multiRow = (
        params: t.QueryParams = {}, where: t.NavigationContext = this.context
    ): void => {
        where.history.pushPath({
            pathname: `/api/${this.context.value.packId}/${this.context.value.actorId}`,
            params: Object.assign(this.multiRowParams(this.defaultParams() as t.QueryParams), params),
        });
    }

    parseClone = (clone: string): t.StateClone => {
        return this.parser.parse(clone) as t.StateClone;
    }

    preprocess = (
        preprocessor: string, preprocessedStack: t.PreprocessedStack = {}
    ): t.QueryParams => {
        if (!this.context.filled(preprocessor)) return preprocessedStack;
        Lino;
        let fn = eval(preprocessor), ret;
        if (this.context.filled(fn)) ret = fn(this.context, preprocessedStack);
        if (this.context.filled(ret) && ret instanceof Object) Object.assign(
            preprocessedStack, ret);
        return preprocessedStack;
    }

    pvArray = (): any[] => {
        let pvObject = this.context.dataContext.mutableContext.param_values,
            fields = Object.keys(pvObject);
        return this.context.static.actorData.params_fields.map((f_name) => {
            let value;
            if (fields.includes(f_name + "Hidden")) value = pvObject[f_name + "Hidden"]
            else value = pvObject[f_name];
            if (value === undefined) value = null;
            return value
        })
    }

    checkAndRunAction = async (kwargs: t.ArgsRunAction): Promise<void> => {
        if (['grid', 'detail', 'show'].includes(kwargs[constants.URL_PARAM_ACTION_NAME]) || !kwargs.clickCatch)
            return await this.runAction(kwargs);
        const clone: t.StateClone = this.cloneState();
        delete kwargs.clickCatch;
        clone.runnable = kwargs;
        window.open(`#${this.context.value.path}?${this.parser.stringify({clone: clone}, true)}`);
    }

    findUniqueAction = (action_name: string): t.Action => {
        return (Object.values(this.context.APP.state.site_data.action_definitions) as t.Action[])
        .filter(a => action_name === a[constants.URL_PARAM_ACTION_NAME])[0];
    }

    runAction = async ({action_full_name, actorId, status, sr = [], rowIndex, default_record_id,
        response_callback, clickCatch = false, pollContext = false
    }: t.ArgsRunAction): Promise<void> => {
        const {action, preprocessedStack} = this.getAction(action_full_name);

        let execute_args: t.ArgsExecute = {
            action: action,
            actorId: actorId,
            response_callback: response_callback || this.getCallback(action[constants.URL_PARAM_ACTION_NAME]),
            rowIndex: rowIndex,
            status: status,
            preprocessedStack: preprocessedStack,
            pollContext: pollContext,
        };

        if (status && status.rqdata && status.xcallback) {
            await this.executeAction(execute_args);
            return;
        }

        if (this.context.filled(sr) && !Array.isArray(sr)) sr = [sr];
        preprocessedStack[constants.URL_PARAM_SELECTED] = sr;

        let actorData = this.context.static.actorData;
        if (!actorData || actorData.id !== actorId)
            actorData = await this.context.getActorData(actorId);

        if (!preprocessedStack[constants.URL_PARAM_SELECTED].length) {
            if (this.context.filled(default_record_id))
                preprocessedStack[constants.URL_PARAM_SELECTED] = ([default_record_id] as number[] | [string])
            else if (this.context.filled(actorData.default_record_id))
                preprocessedStack[constants.URL_PARAM_SELECTED] = [actorData.default_record_id];
        }

        if (status)
            this.context.pushStatus(status, preprocessedStack, actorData);

        if (action.select_rows && !preprocessedStack[constants.URL_PARAM_SELECTED].length)
            preprocessedStack[constants.URL_PARAM_SELECTED] = this.context.value[constants.URL_PARAM_SELECTED];

        if (['grid', 'detail', 'show'].includes(action[constants.URL_PARAM_ACTION_NAME])) {
            if (this.context.value.hasActor && actorId === this.context.static.actorData.id) {
                // TODO: Figure out what other members should be inherited!
                Object.assign(preprocessedStack, {
                    [constants.URL_PARAM_PARAM_VALUES]: this.context.value[
                        constants.URL_PARAM_PARAM_VALUES]});
            }
            delete preprocessedStack.callback;
            let path = {
                pathname: this.URLAppendPKFromSR(`/api/${actorId.split(".").join("/")}`, preprocessedStack[constants.URL_PARAM_SELECTED]),
                params: preprocessedStack
            }
            this.context.history.pushPath(path, {clickCatch: clickCatch});
            return;
        }
        else if (action.window_action) {
            this.context.APP.dialogFactory.create(this, execute_args);
            return;
        }
        else {
            await this.executeAction(execute_args);
        }
    }

    singleRow = (
        event?: any, pk?: number | string,
        where: t.NavigationContext = this.context,
        status: any = {}
    ): void => {
        if (!this.context.static.actorData.detail_action) {
            console.warn(this.context.static.actorData.id + ' has no attribute detail_action');
            return
        }
        if (pk === undefined) {
            pk = event.data[this.context.static.actorData.pk_index];
        }
        if (pk !== undefined) {
            let params: t.QueryParams = this.defaultStaticParams();
            params[constants.URL_PARAM_PARAM_VALUES] = this.context.value[
                constants.URL_PARAM_PARAM_VALUES];
            // console.warn("20241010", params, status);
            where.history.pushPath({
                pathname: `/api/${this.context.value.packId}/${this.context.value.actorId}/${pk}`,
                params: params,
            }, status);
        }
    }

    stringifyClone = (clone: t.StateClone): string => {
        return this.parser.stringify(clone, true);
    }

    submit = async ({cellInfo}: {cellInfo?: t.CellInfo}): Promise<void> => {
        let rowIndex: number | "detail" = constants.DISPLAY_MODE_DETAIL;
        if (cellInfo !== undefined) rowIndex = cellInfo.rowIndex;
        if (!this.context.dataContext.isModified(rowIndex)) {
            if (!cellInfo) this.context.APP.toast.show({
                severity: "info",
                summary: "N/A",
                detail: this.ex.i18n.t("No modified data detected.")
            });
            return;
        }

        let dataContext = this.context.dataContext,
            ad = this.context.static.actorData,
            runnable: t.ArgsRunAction = {
                action_full_name: "", pollContext: true, actorId: ad.id};

        if (cellInfo === undefined) dataContext.root.setState({loading: true});

        if (cellInfo !== undefined) {
            let pk = dataContext.mutableContext.rows[rowIndex][ad.pk_index],
                phantom_row = pk === null;

            runnable.action_full_name = phantom_row ? ad.grid_post : ad.update_action;
            runnable[constants.URL_PARAM_SELECTED] = phantom_row ? [] : [pk];
            runnable.rowIndex = rowIndex;

            runnable.response_callback = (data) => {
                if (data.master_data && this.context.isSlave) {
                    const masterContext = this.context.parent.dataContext;
                    masterContext.updateState(Object.assign(
                        masterContext.mutableContext.data, data.master_data));
                }
                if (data.rows !== undefined) {
                    if (phantom_row) {
                        dataContext.mutableContext.rows.push(
                            dataContext.contextBackup.rows[rowIndex]);
                        dataContext.contextBackup.rows.push(
                            this.ex._.cloneDeep(dataContext.contextBackup.rows[rowIndex]));
                        dataContext.mutableContext.count += 1;
                        dataContext.contextBackup.count += 1;
                        dataContext.mutableContext.modifiedRows[rowIndex as number + 1] = [];
                    }
                    dataContext.mutableContext.rows[rowIndex] = data.rows[0];
                    dataContext.contextBackup.rows[rowIndex] = this.ex._.cloneDeep(data.rows[0]);
                    dataContext.mutableContext.modifiedRows[rowIndex] = []; // Mark unmodified!

                    dataContext.updateState({});
                }
            }
        } else
        if (this.context.contextType === constants.CONTEXT_TYPE_SINGLE_ROW) {
            runnable.action_full_name = ad.submit_detail;
            runnable[constants.URL_PARAM_SELECTED] = this.context.value[constants.URL_PARAM_SELECTED];
        } else
        if (this.context.contextType === constants.CONTEXT_TYPE_TEXT_FIELD) {
            this.XHRPutPost({path: this.context.value.path.slice(1),
                body: Object.assign({}, {[constants.URL_PARAM_ACTION_NAME]: "submit_detail"},
                dataContext.mutableContext.data), response_callback: (data) => {
                    if (data.success) {
                        dataContext.contextBackup.data = this.ex._.cloneDeep(
                            dataContext.mutableContext.data);
                        dataContext.mutableContext.modified = [];
                    }
                }}, "PUT")
            return;
        } else
        if (this.context.contextType === constants.CONTEXT_TYPE_ACTION) {
            runnable.action_full_name = ad.submit_insert;
            runnable.response_callback = (data) => {
                // if (data.close_window) ;
            }
        } else throw Error("Unknown client state");

        this.runAction(runnable);
    }

    submitDetailCallback: t.ResponseCallback = (data) => {
        let dataContext = this.context.dataContext;

        if (data.success) {
            dataContext.backupContext(data.data_record);
            dataContext.mutableContext.modified = [];
            dataContext.updateState(data.data_record);
            Object.values(dataContext.refStore.virtualLeaves).forEach(elem => (
                (elem as React.Component).setState(
                    {key: this.context.newSlug().toString()})));
        }
        dataContext.root.setState({loading: false});
        this.context.history.replaceState({editing_mode: false});
        // consider this situation as signIn since user language may have been changed
        if (this.context.static.actorData.id === 'users.Me')
            this.context.APP.reset(true);
    }

    submitFiles = (dataParams: t.DataParams): void => {
        let uhe = this.context.dataContext.mutableContext.UploadHandlerEvent;

        if (this.context.filled(uhe)) {
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            const {files, options} = uhe;
            Object.values(files).forEach((file: File) => {
                formData.append(options.props.name, file, file.name);
            });
            Object.keys(dataParams).forEach((name) => {
                if (this.context.filled(dataParams[name])) {
                    let value = dataParams[name];
                    if (Array.isArray(value)) value.forEach(v => formData.append(name, v))
                    else formData.append(name, value)
                }
            });

            xhr.onreadystatechange = async () => {
                if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
                    this.context.dataContext.mutableContext.UploadHandlerEvent = null;
                    await this.handleActionResponse({response: JSON.parse(xhr.responseText)});
                }
            }

            xhr.open('POST', options.props.url, true);

            xhr.withCredentials = options.props.withCredentials;

            xhr.send(formData);
        }
    }

    update = ({values, elem, col, windowType = constants.WINDOW_TYPE_DETAIL}: {
        values: t.Data, elem?: any, col?: any, windowType?: t.WindowType
    }): void => {
        let dataContext = this.context.dataContext;
        if (windowType === constants.WINDOW_TYPE_PARAMS) {
            Object.assign(dataContext.mutableContext.param_values, values);
            this.context.history.replace({
                [constants.URL_PARAM_PARAM_VALUES]: this.pvArray()});
        } else if (this.context.contextType === constants.CONTEXT_TYPE_MULTI_ROW) {
            let i = dataContext.mutableContext.modifiedRows[col.rowIndex].indexOf(elem.fields_index),
                noMod = Object.values(values)[0] === dataContext.contextBackup.rows[col.rowIndex][elem.fields_index];
            if (i < 0 && !noMod) {
                dataContext.mutableContext.modifiedRows[col.rowIndex].push(elem.fields_index)
            } else if (i > -1 && noMod) dataContext.mutableContext.modifiedRows[col.rowIndex].splice(i, 1);
            Object.assign(dataContext.mutableContext.rows[col.rowIndex], values);
        } else {
            let i = dataContext.mutableContext.modified.indexOf(elem.name);

            if (i < 0) {
                if (dataContext.contextBackup.data[elem.name] !== Object.values(values)[0])
                    dataContext.mutableContext.modified.push(elem.name);
            } else if (dataContext.contextBackup.data[elem.name] === Object.values(values)[0])
                dataContext.mutableContext.modified.splice(i, 1);

            Object.assign(dataContext.mutableContext.data, values);
        }
    }

    XHRPutPost = async (
        {path, body, signal, silent=false, response_callback}: t.ArgsFetchXHR,
        method: 'PUT' | 'POST'
    ): Promise<void> => {
        if (!silent) this.context.APP.setLoadMask();
        this.ex.fetchPolyfill(path, {
            method: method,
            body: new URLSearchParams(this.ex.queryString.default.stringify(body)),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',// 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            signal: signal,
        }).then(this.handleAjaxResponse).then(async (data) => {
            await this.handleActionResponse({response: data,
                response_callback: response_callback})});
    }
}
