import { CustomJSHover } from "@bokehjs/models/tools/inspectors/customjs_hover";
export class BaseFormatter extends CustomJSHover {
    static __name__ = "BaseFormatter";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "bokehmol.models.base_formatter";
    static {
        this.define(({ Int }) => ({
            width: [Int, 160],
            height: [Int, 120],
        }));
    }
    makeSVGElement() {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
        svg.setAttribute("xmlns:xlink", "http://www.w3.org/1999/xlink");
        svg.setAttributeNS(null, "width", "" + this.width);
        svg.setAttributeNS(null, "height", "" + this.height);
        return svg;
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
        return this.draw_svg(value);
    }
}
//# sourceMappingURL=base_formatter.js.map