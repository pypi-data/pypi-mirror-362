import { BaseHover, BaseHoverView } from "./base_hover";
import { SmilesDrawerFormatter } from "./smilesdrawer_formatter";
export class SmilesDrawerHoverView extends BaseHoverView {
    static __name__ = "SmilesDrawerHoverView";
    initialize() {
        super.initialize();
        const { formatters, smiles_column, width, height, mols_per_row, theme, background_colour, mol_options, reaction_options, } = this.model;
        // @ts-expect-error
        formatters["@" + smiles_column] = new SmilesDrawerFormatter({
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
export class SmilesDrawerHover extends BaseHover {
    static __name__ = "SmilesDrawerHover";
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "bokehmol.models.smilesdrawer_hover";
    static {
        this.prototype.default_view = SmilesDrawerHoverView;
        this.define(({ Str, Dict, Unknown }) => ({
            theme: [Str, "light"],
            background_colour: [Str, "transparent"],
            mol_options: [Dict(Unknown), {}],
            reaction_options: [Dict(Unknown), {}],
        }));
        this.register_alias("smiles_hover", () => new SmilesDrawerHover());
    }
    tool_name = "SmilesDrawer Hover";
}
//# sourceMappingURL=smilesdrawer_hover.js.map