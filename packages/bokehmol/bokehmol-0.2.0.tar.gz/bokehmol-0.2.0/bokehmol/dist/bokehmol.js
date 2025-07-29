'use strict';
/*!
 * Copyright (c) Anaconda, Inc., and Bokeh Contributors
 * All rights reserved.
 * 
 * Redistribution and use in source and binary forms, with or without modification,
 * are permitted provided that the following conditions are met:
 * 
 * Redistributions of source code must retain the above copyright notice,
 * this list of conditions and the following disclaimer.
 * 
 * Redistributions in binary form must reproduce the above copyright notice,
 * this list of conditions and the following disclaimer in the documentation
 * and/or other materials provided with the distribution.
 * 
 * Neither the name of Anaconda nor the names of any contributors
 * may be used to endorse or promote products derived from this software
 * without specific prior written permission.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 */
(function(root, factory) {
  factory(root["Bokeh"], undefined);
})(this, function(Bokeh, version) {
  let define;
  return (function(modules, entry, aliases, externals) {
    const bokeh = typeof Bokeh !== "undefined" ? (version != null ? Bokeh[version] : Bokeh) : null;
    if (bokeh != null) {
      return bokeh.register_plugin(modules, entry, aliases);
    } else {
      throw new Error("Cannot find Bokeh" + (version != null ? " " + version : "") + ". You have to load it prior to loading plugins.");
    }
  })
({
"c27055c896": /* index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    const tslib_1 = require("tslib");
    const bokehmol = tslib_1.__importStar(require("2fbbcedd89") /* ./models */);
    exports.bokehmol = bokehmol;
    const base_1 = require("@bokehjs/base");
    (0, base_1.register_models)(bokehmol);
},
"2fbbcedd89": /* models/index.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    var base_formatter_1 = require("bdbba644e6") /* ./base_formatter */;
    __esExport("BaseFormatter", base_formatter_1.BaseFormatter);
    var base_hover_1 = require("b3aabca0fa") /* ./base_hover */;
    __esExport("BaseHover", base_hover_1.BaseHover);
    var rdkit_formatter_1 = require("66b72b8836") /* ./rdkit_formatter */;
    __esExport("RDKitFormatter", rdkit_formatter_1.RDKitFormatter);
    var rdkit_hover_1 = require("db381e1cc8") /* ./rdkit_hover */;
    __esExport("RDKitHover", rdkit_hover_1.RDKitHover);
    var smilesdrawer_formatter_1 = require("be6f45e05e") /* ./smilesdrawer_formatter */;
    __esExport("SmilesDrawerFormatter", smilesdrawer_formatter_1.SmilesDrawerFormatter);
    var smilesdrawer_hover_1 = require("6c967671db") /* ./smilesdrawer_hover */;
    __esExport("SmilesDrawerHover", smilesdrawer_hover_1.SmilesDrawerHover);
},
"bdbba644e6": /* models/base_formatter.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const customjs_hover_1 = require("@bokehjs/models/tools/inspectors/customjs_hover");
    const combinesvg_1 = require("01840ae548") /* ./combinesvg */;
    class BaseFormatter extends customjs_hover_1.CustomJSHover {
        constructor(attrs) {
            super(attrs);
        }
        makeSVGElement() {
            const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
            svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
            svg.setAttributeNS(null, "width", "" + this.width);
            svg.setAttributeNS(null, "height", "" + this.height);
            return svg;
        }
        draw_grid(smiles_array) {
            const images = [];
            smiles_array.forEach((smiles) => {
                let svg = this.draw_svg(smiles);
                images.push(svg);
            });
            return (0, combinesvg_1.combineSVGs)(images, this.width, this.height, this.mols_per_row);
        }
        // @ts-expect-error
        draw_svg(smiles) {
            const el = this.makeSVGElement();
            const svg = el.outerHTML;
            el.remove();
            return svg;
        }
        format(value, format, special_vars) {
            format;
            special_vars;
            return Array.isArray(value) ? this.draw_grid(value) : this.draw_svg(value);
        }
    }
    exports.BaseFormatter = BaseFormatter;
    _a = BaseFormatter;
    BaseFormatter.__name__ = "BaseFormatter";
    BaseFormatter.__module__ = "bokehmol.models.base_formatter";
    (() => {
        _a.define(({ Int }) => ({
            width: [Int, 160],
            height: [Int, 120],
            mols_per_row: [Int, 5],
        }));
    })();
},
"01840ae548": /* models/combinesvg.js */ function _(require, module, exports, __esModule, __esExport) {
    __esModule();
    exports.combineSVGs = combineSVGs;
    function combineSVGs(images, width, height, maxMolsRow) {
        let grid = [];
        let maxWidth = width;
        let maxHeight = height;
        const parser = new DOMParser();
        for (let i = 0; i < images.length; i++) {
            let svg = images[i];
            let imgWidth = width;
            let imgHeight = height;
            // handle RDKit's edge case when width or height is set to -1
            if ((width < 0) || (height < 0)) {
                // parse directly from SVG element
                let el = parser.parseFromString(svg, 'image/svg+xml').firstChild;
                if (width < 0) {
                    // @ts-expect-error
                    imgWidth = el.width.baseVal.value;
                    if (imgWidth > maxWidth) {
                        maxWidth = imgWidth;
                    }
                    else {
                        imgWidth = maxWidth;
                    }
                }
                if (height < 0)
                    // @ts-expect-error
                    imgHeight = el.height.baseVal.value;
                if (imgHeight > maxHeight) {
                    maxHeight = imgHeight;
                }
                else {
                    imgHeight = maxHeight;
                }
            }
            let x = imgWidth * (i % maxMolsRow);
            let y = imgHeight * Math.floor(i / maxMolsRow);
            let b64dump = btoa(svg);
            grid.push(`<image id="molecule-${i}" transform="translate(${x},${y})" href='data:image/svg+xml;base64,${b64dump}'></image>`);
        }
        const parentWidth = maxWidth * Math.min(maxMolsRow, images.length);
        const parentHeight = maxHeight * Math.ceil(images.length / maxMolsRow);
        return `<svg width="${parentWidth}" height="${parentHeight}">${grid.join("\n")}</svg>`;
    }
},
"b3aabca0fa": /* models/base_hover.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const dom_1 = require("@bokehjs/core/dom");
    const templating_1 = require("@bokehjs/core/util/templating");
    const types_1 = require("@bokehjs/core/util/types");
    const hover_tool_1 = require("@bokehjs/models/tools/inspectors/hover_tool");
    const icons_css_1 = require("@bokehjs/styles/icons.css");
    class BaseHoverView extends hover_tool_1.HoverToolView {
        _render_tooltips(ds, vars) {
            const { tooltips, smiles_column } = this.model;
            const i = vars.index;
            let user_tooltip = tooltips;
            if (user_tooltip === null) {
                user_tooltip = "";
            }
            if (!(0, types_1.isString)(user_tooltip)) {
                const template = this._template_el ?? (
                // @ts-ignore
                this._template_el = this._create_template(user_tooltip));
                // @ts-ignore
                user_tooltip = this._render_template(template, user_tooltip, ds, vars).outerHTML;
            }
            const mol_tooltip = "<div>@" + smiles_column + "{custom}</div>" + user_tooltip;
            const content = (0, templating_1.replace_placeholders)({ html: mol_tooltip }, ds, i, this.model.formatters, vars);
            return (0, dom_1.div)(content);
        }
    }
    exports.BaseHoverView = BaseHoverView;
    BaseHoverView.__name__ = "BaseHoverView";
    class BaseHover extends hover_tool_1.HoverTool {
        get computed_icon() {
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAWCAMAAADzapwJAAAAt1BMVEUAAAAAAAArKyskJCQcHBwrKyscHBwmJiYjIyMhISEgICAfHx8dHR0kJCQiIiIhISEhISEgICAkJCQkJCQjIyMiIiIiIiIhISEkJCQjIyMiIiIiIiIjIyMjIyMkJCQjIyMiIiIkJCQhISEjIyMiIiIiIiIiIiIkJCQjIyMiIiIiIiIiIiIiIiIhISEjIyMjIyMiIiIiIiIjIyMiIiIiIiIhISEiIiIiIiIiIiIiIiIhISEjIyP///9o30WSAAAAPHRSTlMAAQYHCQwSFBYXGBkaKy0uLzAxMjM0NTY5UVJTV1hdYHJyc3V3eHmBk5SVlpeZmpucnaqtrrCytLa7wMBTv07WAAAAAWJLR0Q8p2phzwAAAKRJREFUGBmtwQkagUAAgNF/ZAtZo2yRIrusofvfi+ab0gG8xx85gS8FDjlabJuS/db4WQ1RRksy+p3ZRZpxbZA6t8gYJxRzTc7WQhKPCjnlSJDwXEIdRQ9xPRKeS+eAcurjeiTEo8JhgNTdU44EUm9D9SlIRDV2FkrYZjHhazrHOJLS7xReRSi+CtzqZJYjmiUoNRn7/GixbUr2WyPHCXwpcPifD0UBD3u/QqniAAAAAElFTkSuQmCC";
        }
        constructor(attrs) {
            super(attrs);
            this.tool_icon = icons_css_1.tool_icon_hover;
        }
    }
    exports.BaseHover = BaseHover;
    _a = BaseHover;
    BaseHover.__name__ = "BaseHover";
    BaseHover.__module__ = "bokehmol.models.base_hover";
    (() => {
        _a.prototype.default_view = BaseHoverView;
        _a.define(({ Str, Int }) => ({
            smiles_column: [Str, "SMILES"],
            width: [Int, 160],
            height: [Int, 120],
            mols_per_row: [Int, 3],
        }));
        _a.override({
            tooltips: [],
        });
    })();
},
"66b72b8836": /* models/rdkit_formatter.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const base_formatter_1 = require("bdbba644e6") /* ./base_formatter */;
    class RDKitFormatter extends base_formatter_1.BaseFormatter {
        constructor(attrs) {
            super(attrs);
        }
        initialize() {
            super.initialize();
            this.onRDKitReady(true, false, () => {
                // @ts-expect-error
                initRDKitModule().then((RDKitModule) => {
                    this.RDKitModule = RDKitModule;
                    console.log("RDKit version: " + RDKitModule.version());
                });
            });
        }
        onRDKitReady(init, lib, callback) {
            this.hasLoadedRDKit(init, lib) ? callback() : setTimeout(() => {
                this.onRDKitReady(init, lib, callback);
            }, 100);
        }
        hasLoadedRDKit(init, lib) {
            // @ts-expect-error
            return (init ? typeof initRDKitModule !== "undefined" : true)
                && (lib ? typeof this.RDKitModule !== "undefined" : true);
        }
        setupRDKitOptions() {
            this.onRDKitReady(true, true, () => {
                this.RDKitModule.prefer_coordgen(this.prefer_coordgen);
            });
            this.json_mol_opts = JSON.stringify({
                removeHs: this.remove_hs,
                sanitize: this.sanitize,
                kekulize: this.kekulize,
            });
            this.json_draw_opts = JSON.stringify({
                width: this.width,
                height: this.height,
                ...this.draw_options,
            });
            return this.json_draw_opts;
        }
        draw_svg(smiles) {
            const draw_opts = this.json_draw_opts ?? this.setupRDKitOptions();
            var mol;
            this.onRDKitReady(true, true, () => {
                mol = this.RDKitModule.get_mol(smiles, this.json_mol_opts);
            });
            // @ts-expect-error
            if (typeof mol === "undefined") {
                console.log("Attempting to display structures before RDKit has been loaded.");
            }
            else if (mol !== null && mol.is_valid()) {
                const svg = mol.get_svg_with_highlights(draw_opts);
                mol.delete();
                return svg;
            }
            return super.draw_svg(smiles);
        }
    }
    exports.RDKitFormatter = RDKitFormatter;
    _a = RDKitFormatter;
    RDKitFormatter.__name__ = "RDKitFormatter";
    RDKitFormatter.__module__ = "bokehmol.models.rdkit_formatter";
    (() => {
        _a.define(({ Bool, Dict, Unknown }) => ({
            prefer_coordgen: [Bool, true],
            remove_hs: [Bool, true],
            sanitize: [Bool, true],
            kekulize: [Bool, true],
            draw_options: [Dict(Unknown), {}],
        }));
    })();
},
"db381e1cc8": /* models/rdkit_hover.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const base_hover_1 = require("b3aabca0fa") /* ./base_hover */;
    const rdkit_formatter_1 = require("66b72b8836") /* ./rdkit_formatter */;
    class RDKitHoverView extends base_hover_1.BaseHoverView {
        initialize() {
            super.initialize();
            const { formatters, smiles_column, width, height, mols_per_row, prefer_coordgen, remove_hs, sanitize, kekulize, draw_options } = this.model;
            // @ts-expect-error
            formatters["@" + smiles_column] = new rdkit_formatter_1.RDKitFormatter({
                width: width,
                height: height,
                mols_per_row: mols_per_row,
                prefer_coordgen: prefer_coordgen,
                remove_hs: remove_hs,
                sanitize: sanitize,
                kekulize: kekulize,
                draw_options: draw_options,
            });
        }
    }
    exports.RDKitHoverView = RDKitHoverView;
    RDKitHoverView.__name__ = "RDKitHoverView";
    class RDKitHover extends base_hover_1.BaseHover {
        get computed_icon() {
            return "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQBAMAAADt3eJSAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAFVBMVEXc3NwUFP8UPP9kZP+MjP+0tP////9ZXZotAAAAAXRSTlMAQObYZgAAAAFiS0dEBmFmuH0AAAAHdElNRQfmAwsPGi+MyC9RAAAAQElEQVQI12NgQABGQUEBMENISUkRLKBsbGwEEhIyBgJFsICLC0iIUdnExcUZwnANQWfApKCK4doRBsKtQFgKAQC5Ww1JEHSEkAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMi0wMy0xMVQxNToyNjo0NyswMDowMDzr2J4AAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjItMDMtMTFUMTU6MjY6NDcrMDA6MDBNtmAiAAAAAElFTkSuQmCC";
        }
        constructor(attrs) {
            super(attrs);
            this.tool_name = "RDKit Hover";
        }
    }
    exports.RDKitHover = RDKitHover;
    _a = RDKitHover;
    RDKitHover.__name__ = "RDKitHover";
    RDKitHover.__module__ = "bokehmol.models.rdkit_hover";
    (() => {
        _a.prototype.default_view = RDKitHoverView;
        _a.define(({ Bool, Dict, Unknown }) => ({
            prefer_coordgen: [Bool, true],
            remove_hs: [Bool, true],
            sanitize: [Bool, true],
            kekulize: [Bool, true],
            draw_options: [Dict(Unknown), {}],
        }));
        _a.register_alias("rdkit_hover", () => new _a());
    })();
},
"be6f45e05e": /* models/smilesdrawer_formatter.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const base_formatter_1 = require("bdbba644e6") /* ./base_formatter */;
    class SmilesDrawerFormatter extends base_formatter_1.BaseFormatter {
        constructor(attrs) {
            super(attrs);
        }
        initialize() {
            super.initialize();
            this.onSmiDrawerReady(true, false, () => {
                // @ts-expect-error
                this.SmiDrawer = SmiDrawer;
            });
        }
        onSmiDrawerReady(init, lib, callback) {
            this.hasLoadedSmiDrawer(init, lib) ? callback() : setTimeout(() => {
                this.onSmiDrawerReady(init, lib, callback);
            }, 100);
        }
        hasLoadedSmiDrawer(init, lib) {
            // @ts-expect-error
            return (init ? typeof SmiDrawer !== "undefined" : true)
                && (lib ? typeof this.SmiDrawer !== "undefined" : true);
        }
        makeSVGElement() {
            const el = super.makeSVGElement();
            el.style.backgroundColor = this.background_colour;
            return el;
        }
        setupDrawer() {
            this.onSmiDrawerReady(true, true, () => {
                this.drawer = new this.SmiDrawer(this.mol_options, this.reaction_options);
            });
            return this.drawer;
        }
        draw_svg(smiles) {
            const el = this.makeSVGElement();
            this.onSmiDrawerReady(true, true, () => {
                const sd = this.drawer ?? this.setupDrawer();
                sd.draw(smiles, el, this.theme);
            });
            const svg = el.outerHTML;
            el.remove();
            return svg;
        }
    }
    exports.SmilesDrawerFormatter = SmilesDrawerFormatter;
    _a = SmilesDrawerFormatter;
    SmilesDrawerFormatter.__name__ = "SmilesDrawerFormatter";
    SmilesDrawerFormatter.__module__ = "bokehmol.models.smilesdrawer_formatter";
    (() => {
        _a.define(({ Str, Dict, Unknown }) => ({
            theme: [Str, "light"],
            background_colour: [Str, "transparent"],
            mol_options: [Dict(Unknown), {}],
            reaction_options: [Dict(Unknown), {}],
        }));
    })();
},
"6c967671db": /* models/smilesdrawer_hover.js */ function _(require, module, exports, __esModule, __esExport) {
    var _a;
    __esModule();
    const base_hover_1 = require("b3aabca0fa") /* ./base_hover */;
    const smilesdrawer_formatter_1 = require("be6f45e05e") /* ./smilesdrawer_formatter */;
    class SmilesDrawerHoverView extends base_hover_1.BaseHoverView {
        initialize() {
            super.initialize();
            const { formatters, smiles_column, width, height, mols_per_row, theme, background_colour, mol_options, reaction_options, } = this.model;
            // @ts-expect-error
            formatters["@" + smiles_column] = new smilesdrawer_formatter_1.SmilesDrawerFormatter({
                width: width,
                height: height,
                mols_per_row: mols_per_row,
                theme: theme,
                background_colour: background_colour,
                mol_options: mol_options,
                reaction_options: reaction_options,
            });
        }
    }
    exports.SmilesDrawerHoverView = SmilesDrawerHoverView;
    SmilesDrawerHoverView.__name__ = "SmilesDrawerHoverView";
    class SmilesDrawerHover extends base_hover_1.BaseHover {
        constructor(attrs) {
            super(attrs);
            this.tool_name = "SmilesDrawer Hover";
        }
    }
    exports.SmilesDrawerHover = SmilesDrawerHover;
    _a = SmilesDrawerHover;
    SmilesDrawerHover.__name__ = "SmilesDrawerHover";
    SmilesDrawerHover.__module__ = "bokehmol.models.smilesdrawer_hover";
    (() => {
        _a.prototype.default_view = SmilesDrawerHoverView;
        _a.define(({ Str, Dict, Unknown }) => ({
            theme: [Str, "light"],
            background_colour: [Str, "transparent"],
            mol_options: [Dict(Unknown), {}],
            reaction_options: [Dict(Unknown), {}],
        }));
        _a.register_alias("smiles_hover", () => new _a());
    })();
},
}, "c27055c896", {"index":"c27055c896","models/index":"2fbbcedd89","models/base_formatter":"bdbba644e6","models/combinesvg":"01840ae548","models/base_hover":"b3aabca0fa","models/rdkit_formatter":"66b72b8836","models/rdkit_hover":"db381e1cc8","models/smilesdrawer_formatter":"be6f45e05e","models/smilesdrawer_hover":"6c967671db"}, {});});
//# sourceMappingURL=bokehmol.js.map
