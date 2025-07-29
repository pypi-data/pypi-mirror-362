export const name = "LinoEditor";

import React from "react";
import { RegisterImportPool, Component, URLContextType } from "./Base";
import { quillMention, quillToolbar, imageHandler, overrideImageButtonHandler,
    invokeRefInsert} from "./quillmodules";
import { LeafComponentInput } from "./LinoComponentUtils";
import * as constants from "./constants";

let ex; const exModulePromises = ex = {
    AbortController: import(/* webpackChunkName: "AbortController_LinoEditor" */"abort-controller"),
    prButton: import(/* webpackChunkName: "prButton_LinoEditor" */"primereact/button"),
    prEditor: import(/* webpackChunkName: "prEditor_LinoEditor" */"primereact/editor"),
    prDialog: import(/* webpackChunkName: "prDialog_LinoEditor" */"primereact/dialog"),
    i18n: import(/* webpackChunkName: "i18n_LinoEditor" */"./i18n"),
}
RegisterImportPool(ex);


export class LinoEditor extends LeafComponentInput {
    static requiredModules = ["AbortController", "prButton", "prEditor",
        "prDialog", "i18n"].concat(LeafComponentInput.requiredModules);
    static iPool = Object.assign(ex, LeafComponentInput.iPool.copy());
    async prepare() {
        await super.prepare();
        this.controller = new this.ex.AbortController.default();
        this.ex.i18n = this.ex.i18n.default;
    }

    constructor(props) {
        super(props);
        this.state = {...this.state,
                      plain: props.elem.field_options.format === "plain"}

        this.closeEditor = this.closeEditor.bind(this);
        this.onGlobalKeyDown = this.onGlobalKeyDown.bind(this);
        this.onTextChange = this.onTextChange.bind(this);
    }

    onReady() {
        window.addEventListener('keydown', this.onGlobalKeyDown);
    }

    componentWillUnmount() {
        window.removeEventListener('keydown', this.onGlobalKeyDown);
    }

    onGlobalKeyDown(e) {
        if (e.code == 'Escape') this.closeEditor(e);
    }

    closeEditor(e) {
        const { c } = this;
        const DO = () => {
            c.history.pushPath({pathname: `/api/${c.value.packId}/${c.value.actorId}/${c.value.pk}`})
        }
        if (!c.isModified()) {DO()} else
            c.actionHandler.discardModDConfirm({agree: DO});
    }

    headerExtend() {
        return <>
            {quillToolbar.commonHeader(this)}
            <span className="ql-formats">
                <button type='button'
                    onClick={e => this.c.actionHandler.submit({})}
                    aria-label='Submit changes'>
                    <i className="pi pi-save"></i></button>
                <button type='button'
                    onClick={this.closeEditor}
                    aria-label='Close window'>
                    <i className="pi pi-times"></i></button>
            </span>
        </>
    }

    onTextChange(e) {
        // cleans up the trailing new line (\n)
        const plainValue = e.textValue.slice(0, -1);
        let value = (this.state.plain ? plainValue : e.htmlValue ) || "";
        this.update({[this.dataKey]: value});
        this.setState({});
    }

    render () {
        if (!this.state.ready) return null;
        return <URLContextType.Consumer>
            {value => {
                const { APP } = value.controller;
                const modules = {
                    mention: quillMention({
                        silentFetch: value.controller.actionHandler.silentFetch,
                        signal: value.controller.signal,
                        mentionValues: value.controller.mentionValues})
                }
                if (APP.state.site_data.installed_plugins.includes('uploads'))
                    modules.imageDropAndPaste = {handler: imageHandler};

                return <div className="l-editor"
                    onKeyDown={(e) => {
                        if ((e.ctrlKey || e.metaKey) && e.code === "KeyS") {
                            e.stopPropagation();
                            e.preventDefault();
                            this.c.actionHandler.submit({});
                        } else if (e.ctrlKey && e.shiftKey && e.code == "KeyL") {
                            e.stopPropagation();
                            e.preventDefault();
                            invokeRefInsert(this);
                        } else if (e.code !== 'Escape') e.stopPropagation();
                    }}>
                    <this.ex.prEditor.Editor
                        headerTemplate={this.headerExtend()}
                        modules={modules}
                        onLoad={e => {
                            this.quill = this.inputEl.getQuill();
                            overrideImageButtonHandler(this.quill);
                        }}
                        onTextChange={this.onTextChange}
                        ref={ref => this.inputEl = ref}
                        style={{background: "#ffffff"}}
                        value={this.context.data[value.fieldName]}/>
                </div>
            }}
        </URLContextType.Consumer>
    }
}
