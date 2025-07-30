# Quick Actions - Configure Your Action menus with hierarchical TOML files bringing your own scripts.

## Configuration
Default config dir on posix is `$HOME/.config/quick_actions`, on windows is `$HOME/Appdata/Local/quick_actions`.

## Install

### Using pip
```sh
> pip install quick-actions
```


### Using nixpkgs
```nix
{
    ...
    inputs = {
        quick-actions = {
            url = "git+https://gitlab.com/leswell/quick-actions";
            inputs.nixpkgs.follows = "nixpkgs";
        };
        ...
    }
}
```

**AND** add the package to system or home-manager `quick-actions.packages.${pkgs.system}.quick-actions`
**OR**
use one of the modules.


## PLANS:
- [ ] Module system? (eg. history module, hyprland module)
- [ ] History for outputs (eg. `script.calculator.qalc.calculator`)
- [ ] Copy result after show
- [ ] State "persist"
- [ ] Profiles, activatable with `--profile` flag, under `config/profiles`, which overwrites defaults
- [ ] `format-before-copy` for actions (_eg. `script.calculator.qalc.calculator` cut the operation, keep only the result_)
- [ ] `format-action-result` for actions (_eg. `colorpicker.hyprpicker`_)
- [ ] hyprland keybinding modules, using `hyprctl binds -j`
- [ ] store most recents for consecutive searches (something like `zoxide`) 
- [ ] Complete the docs / check out wiki
- [ ] Aliases somehow (mayB prefix without arguments, SO rethink prefix)
