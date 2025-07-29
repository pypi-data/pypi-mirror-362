import { BaseFormatter } from "./base_formatter";
export class SmilesDrawerFormatter extends BaseFormatter {
    static __name__ = "SmilesDrawerFormatter";
    SmiDrawer;
    drawer;
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "bokehmol.models.smilesdrawer_formatter";
    static {
        this.define(({ Str, Dict, Unknown }) => ({
            theme: [Str, "light"],
            background_colour: [Str, "transparent"],
            mol_options: [Dict(Unknown), {}],
            reaction_options: [Dict(Unknown), {}],
        }));
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
//# sourceMappingURL=smilesdrawer_formatter.js.map