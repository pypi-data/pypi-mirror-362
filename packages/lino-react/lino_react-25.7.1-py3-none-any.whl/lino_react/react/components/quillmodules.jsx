export const name = "quillmodules";

import 'quill-mention/autoregister';
import 'quill-mention';
import Quill from 'quill';
import QuillImageDropAndPaste from 'quill-image-drop-and-paste';
import React from 'react';
import { RegisterImportPool } from "./Base";

Quill.register('modules/imageDropAndPaste', QuillImageDropAndPaste);

const QuillImageData = QuillImageDropAndPaste.ImageData;

let ex; const exModulePromises = ex = {
    queryString:  import(/* webpackChunkName: "queryString_quillmodules" */"query-string"),
};RegisterImportPool(ex);


export const passInQuill = (quill) => ex.quill = quill;


export const overrideImageButtonHandler = (quill) => {
    passInQuill(quill);
    quill.getModule('toolbar').addHandler('image', (clicked) => {
        if (clicked) {
            let fileInput;
            // fileInput = quill.container.querySelector('input.ql-image[type=file]');
            // if (fileInput == null) {
                fileInput = document.createElement('input');
                fileInput.setAttribute('type', 'file');
                fileInput.setAttribute('accept', 'image/png, image/gif, image/jpeg, image/bmp, image/x-icon');
                fileInput.classList.add('ql-image');
                fileInput.addEventListener('change', (e) => {
                    const files = e.target.files;
                    let file;
                    if (files.length > 0) {
                        file = files[0];
                        const type = file.type;
                        const reader = new FileReader();
                        reader.onload = (e) => {
                            const dataURL = e.target.result;
                            imageHandler(dataURL, type, new QuillImageData(dataURL, type, file.name));
                            fileInput.value = '';
                        }
                        reader.readAsDataURL(file);
                    }
                })
            // }
            fileInput.click();
        }
    })
}

export const imageHandler = (imageDataURL, type, imageData) => {
    const quill = ex.quill;
    let index = (quill.getSelection() || {}).index;
    if (index === undefined || index < 0) index = quill.getLength();
    quill.insertEmbed(index, 'image', imageDataURL);
}

export const quillMention = ({silentFetch, signal, mentionValues}) => {
    function mentionSource(searchTerm, renderList, mentionChar) {
        if (searchTerm.length === 0) {
            let values = mentionValues[mentionChar];
            renderList(values, searchTerm);
        } else {
            ex.resolve(['queryString']).then(({queryString}) => {
                silentFetch({path: `suggestions?${queryString.default.stringify({
                    query: searchTerm, trigger: mentionChar})}`, signal: signal})
                .then(data => renderList(data.suggestions, searchTerm));
            });
        }
    }

    return {
        allowedChars: /^[A-Za-z0-9\s]*$/,
        mentionDenotationChars: window.App.state.site_data.suggestors,
        source: mentionSource,
        listItemClass: "ql-mention-list-item",
        mentionContainerClass: "ql-mention-list-container",
        mentionListClass: "ql-mention-list",
        dataAttributes: ["value", "link", "title", "denotationChar"],
    }
}

const quillToolbarHeaderTemplate = <React.Fragment>
    <span className="ql-formats">
        <select className='ql-header' defaultValue='0'>
            <option value='1'>Heading</option>
            <option value='2'>Subheading</option>
            <option value='0'>Normal</option>
        </select>
        <select className='ql-font'>
            <option defaultValue={true}></option>
            <option value='serif'></option>
            <option value='monospace'></option>
        </select>
    </span>
    <span className="ql-formats">
        <select className="ql-size">
            <option value="small"></option>
            <option defaultValue={true}></option>
            <option value="large"></option>
            <option value="huge"></option>
        </select>
    </span>
    <span className="ql-formats">
        <button className="ql-script" value="sub"></button>
        <button className="ql-script" value="super"></button>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-bold' aria-label='Bold'></button>
        <button type='button' className='ql-italic' aria-label='Italic'></button>
        <button type='button' className='ql-underline' aria-label='Underline'></button>
    </span>
    <span className="ql-formats">
        <select className='ql-color'></select>
        <select className='ql-background'></select>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-list' value='ordered' aria-label='Ordered List'></button>
        <button type='button' className='ql-list' value='bullet' aria-label='Unordered List'></button>
        <select className='ql-align'>
            <option defaultValue={true}></option>
            <option value='center'></option>
            <option value='right'></option>
            <option value='justify'></option>
        </select>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-link' aria-label='Insert Link'></button>
        <button type='button' className='ql-image' aria-label='Insert Image'></button>
        <button type='button' className='ql-code-block' aria-label='Insert Code Block'></button>
    </span>
    <span className="ql-formats">
        <button type='button' className='ql-clean' aria-label='Remove Styles'></button>
    </span>
</React.Fragment>

export const invokeRefInsert = (elem) => {
    const { APP } = elem.props.urlParams.controller;
    const { URLContext } = APP;
    let index = (elem.quill.getSelection() || {}).index;
    if (index === undefined || index < 0)
        index = elem.quill.getLength();
    URLContext.actionHandler.runAction({
        action_full_name: URLContext.actionHandler.findUniqueAction("insert_reference").full_name,
        actorId: "about.About",
        response_callback: (data) => {
            if (data.success)
                elem.quill.insertText(index, data.message);
        }
    });
}

const commonHeader = (elem) => {
    return <>
        {quillToolbarHeaderTemplate}
        <span className="ql-formats">
            <button type='button'
                onClick={(e) => invokeRefInsert(elem)}
                aria-label='Open link dialog'>
                <i className="pi pi-link"></i></button>
        </span>
    </>
}

export const quillToolbar = {
    header: quillToolbarHeaderTemplate,
    commonHeader: commonHeader,
}
