import { BaseFormatter } from "./base_formatter";
export class RDKitFormatter extends BaseFormatter {
    static __name__ = "RDKitFormatter";
    RDKitModule;
    json_draw_opts;
    json_mol_opts;
    constructor(attrs) {
        super(attrs);
    }
    static __module__ = "bokehmol.models.rdkit_formatter";
    static {
        this.define(({ Bool, Dict, Unknown }) => ({
            prefer_coordgen: [Bool, true],
            remove_hs: [Bool, true],
            sanitize: [Bool, true],
            kekulize: [Bool, true],
            draw_options: [Dict(Unknown), {}],
        }));
    }
    initialize() {
        super.initialize();
        this.onRDKitReady(true, false, () => {
            // @ts-expect-error
            initRDKitModule().then((RDKitModule) => {
                this.RDKitModule = RDKitModule;
                console.log("RDKit version: " + RDKitModule.version());
            });
        });
    }
    onRDKitReady(init, lib, callback) {
        this.hasLoadedRDKit(init, lib) ? callback() : setTimeout(() => {
            this.onRDKitReady(init, lib, callback);
        }, 100);
    }
    hasLoadedRDKit(init, lib) {
        // @ts-expect-error
        return (init ? typeof initRDKitModule !== "undefined" : true)
            && (lib ? typeof this.RDKitModule !== "undefined" : true);
    }
    setupRDKitOptions() {
        this.onRDKitReady(true, true, () => {
            this.RDKitModule.prefer_coordgen(this.prefer_coordgen);
        });
        this.json_mol_opts = JSON.stringify({
            removeHs: this.remove_hs,
            sanitize: this.sanitize,
            kekulize: this.kekulize,
        });
        this.json_draw_opts = JSON.stringify({
            width: this.width,
            height: this.height,
            ...this.draw_options,
        });
        return this.json_draw_opts;
    }
    draw_svg(smiles) {
        const draw_opts = this.json_draw_opts ?? this.setupRDKitOptions();
        var mol;
        this.onRDKitReady(true, true, () => {
            mol = this.RDKitModule.get_mol(smiles, this.json_mol_opts);
        });
        // @ts-expect-error
        if (typeof mol === "undefined") {
            console.log("Attempting to display structures before RDKit has been loaded.");
        }
        else if (mol !== null && mol.is_valid()) {
            const svg = mol.get_svg_with_highlights(draw_opts);
            mol.delete();
            return svg;
        }
        return super.draw_svg(smiles);
    }
}
//# sourceMappingURL=rdkit_formatter.js.map