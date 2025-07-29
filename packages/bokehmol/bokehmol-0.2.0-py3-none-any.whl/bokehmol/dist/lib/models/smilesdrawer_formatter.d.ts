import type * as p from "@bokehjs/core/properties";
import type { Dict } from "@bokehjs/core/types";
import { BaseFormatter } from "./base_formatter";
declare namespace smilesdrawer {
    class SmiDrawer {
        constructor(moleculeOptions: object, reactionOptions: object);
        draw(smiles: string, target: SVGElement, theme?: string): void;
    }
}
export declare namespace SmilesDrawerFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseFormatter.Props & {
        theme: p.Property<string>;
        background_colour: p.Property<string>;
        mol_options: p.Property<Dict<unknown>>;
        reaction_options: p.Property<Dict<unknown>>;
    };
}
export interface SmilesDrawerFormatter extends SmilesDrawerFormatter.Attrs {
}
export declare class SmilesDrawerFormatter extends BaseFormatter {
    properties: SmilesDrawerFormatter.Props;
    protected SmiDrawer: typeof smilesdrawer.SmiDrawer;
    protected drawer: smilesdrawer.SmiDrawer;
    constructor(attrs?: Partial<SmilesDrawerFormatter.Attrs>);
    static __module__: string;
    initialize(): void;
    onSmiDrawerReady(init: boolean, lib: boolean, callback: () => void): void;
    hasLoadedSmiDrawer(init: boolean, lib: boolean): boolean;
    makeSVGElement(): SVGElement;
    setupDrawer(): smilesdrawer.SmiDrawer;
    draw_svg(smiles: string): string;
}
export {};
//# sourceMappingURL=smilesdrawer_formatter.d.ts.map