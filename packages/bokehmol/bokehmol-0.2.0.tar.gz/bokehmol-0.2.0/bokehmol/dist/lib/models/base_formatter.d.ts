import { CustomJSHover } from "@bokehjs/models/tools/inspectors/customjs_hover";
import type * as p from "@bokehjs/core/properties";
export declare namespace BaseFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = CustomJSHover.Props & {
        width: p.Property<number>;
        height: p.Property<number>;
        mols_per_row: p.Property<number>;
    };
}
export interface BaseFormatter extends BaseFormatter.Attrs {
}
export declare class BaseFormatter extends CustomJSHover {
    properties: BaseFormatter.Props;
    constructor(attrs?: Partial<BaseFormatter.Attrs>);
    static __module__: string;
    makeSVGElement(): SVGElement;
    draw_grid(smiles_array: string[]): string;
    draw_svg(smiles: string): string;
    format(value: any, format: string, special_vars: {
        [key: string]: unknown;
    }): string;
}
//# sourceMappingURL=base_formatter.d.ts.map