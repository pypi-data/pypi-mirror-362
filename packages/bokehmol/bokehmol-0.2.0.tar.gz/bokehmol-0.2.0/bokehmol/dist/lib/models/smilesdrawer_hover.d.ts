import type * as p from "@bokehjs/core/properties";
import { BaseHover, BaseHoverView } from "./base_hover";
import { SmilesDrawerFormatter } from "./smilesdrawer_formatter";
export declare class SmilesDrawerHoverView extends BaseHoverView {
    model: SmilesDrawerHover;
    initialize(): void;
}
export declare namespace SmilesDrawerHover {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseHover.Props & SmilesDrawerFormatter.Props;
}
export interface SmilesDrawerHover extends SmilesDrawerHover.Attrs {
}
export declare class SmilesDrawerHover extends BaseHover {
    properties: SmilesDrawerHover.Props;
    constructor(attrs?: Partial<SmilesDrawerHover.Attrs>);
    static __module__: string;
    tool_name: string;
}
//# sourceMappingURL=smilesdrawer_hover.d.ts.map