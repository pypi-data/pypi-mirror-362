import type * as p from "@bokehjs/core/properties";
import type { ColumnarDataSource } from "@bokehjs/models/sources/columnar_data_source";
import { HoverTool, HoverToolView, TooltipVars } from "@bokehjs/models/tools/inspectors/hover_tool";
import { BaseFormatter } from "./base_formatter";
export declare class BaseHoverView extends HoverToolView {
    model: BaseHover;
    _render_tooltips(ds: ColumnarDataSource, vars: TooltipVars): HTMLElement | null;
}
export declare namespace BaseHover {
    type Attrs = p.AttrsOf<Props>;
    type Props = HoverTool.Props & BaseFormatter.Props & {
        smiles_column: p.Property<String>;
    };
}
export interface BaseHover extends BaseHover.Attrs {
}
export declare class BaseHover extends HoverTool {
    properties: BaseHover.Props;
    get computed_icon(): string;
    constructor(attrs?: Partial<BaseHover.Attrs>);
    static __module__: string;
    tool_icon: string;
}
//# sourceMappingURL=base_hover.d.ts.map