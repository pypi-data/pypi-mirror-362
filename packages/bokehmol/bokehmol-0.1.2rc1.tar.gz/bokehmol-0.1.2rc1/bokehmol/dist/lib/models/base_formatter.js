import { CustomJSHover } from "@bokehjs/models/tools/inspectors/customjs_hover";
import { combineSVGs } from "./combinesvg";
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
            mols_per_row: [Int, 5],
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
    draw_grid(smiles_array) {
        const images = [];
        smiles_array.forEach((smiles) => {
            let svg = this.draw_svg(smiles);
            images.push(svg);
        });
        return combineSVGs(images, this.width, this.height, this.mols_per_row);
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
//# sourceMappingURL=base_formatter.js.map