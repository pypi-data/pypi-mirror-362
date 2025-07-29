import type * as p from "@bokehjs/core/properties";
import { BaseHover, BaseHoverView } from "./base_hover";
import { RDKitFormatter } from "./rdkit_formatter";
export declare class RDKitHoverView extends BaseHoverView {
    model: RDKitHover;
    initialize(): void;
}
export declare namespace RDKitHover {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseHover.Props & RDKitFormatter.Props;
}
export interface RDKitHover extends RDKitHover.Attrs {
}
export declare class RDKitHover extends BaseHover {
    properties: RDKitHover.Props;
    get computed_icon(): string;
    constructor(attrs?: Partial<RDKitHover.Attrs>);
    static __module__: string;
    tool_name: string;
}
//# sourceMappingURL=rdkit_hover.d.ts.map