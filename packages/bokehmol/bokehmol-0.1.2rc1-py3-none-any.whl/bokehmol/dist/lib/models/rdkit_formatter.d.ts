import type * as p from "@bokehjs/core/properties";
import type { Dict } from "@bokehjs/core/types";
import type { RDKitModule } from "@rdkit/rdkit";
import { BaseFormatter } from "./base_formatter";
export declare namespace RDKitFormatter {
    type Attrs = p.AttrsOf<Props>;
    type Props = BaseFormatter.Props & {
        prefer_coordgen: p.Property<boolean>;
        remove_hs: p.Property<boolean>;
        sanitize: p.Property<boolean>;
        kekulize: p.Property<boolean>;
        draw_options: p.Property<Dict<unknown>>;
    };
}
export interface RDKitFormatter extends RDKitFormatter.Attrs {
}
export declare class RDKitFormatter extends BaseFormatter {
    properties: RDKitFormatter.Props;
    protected RDKitModule: RDKitModule;
    protected json_draw_opts?: string;
    protected json_mol_opts?: string;
    constructor(attrs?: Partial<RDKitFormatter.Attrs>);
    static __module__: string;
    initialize(): void;
    onRDKitReady(init: boolean, lib: boolean, callback: () => void): void;
    hasLoadedRDKit(init: boolean, lib: boolean): boolean;
    setupRDKitOptions(): string;
    draw_svg(smiles: string): string;
}
//# sourceMappingURL=rdkit_formatter.d.ts.map