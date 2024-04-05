script to edit config files then reboot  
config path: /etc/reboot.py/config.ini
#### config example:
```
[General]
targets=test
files=/file-to-edit,/etc/default/grub
```
#### lines in config file need to end with #reboot-<target> for example:
```
GRUB_HIDDEN_TIMEOUT=0 #reboot-grub_no_wait
GRUB_HIDDEN_TIMEOUT=5 #reboot-grub_wait
```
will comment out first line (and uncomment second one) when `reboot.py grub_wait` is run 

#### features:
target autocompletion, `reboot.py t` will be autocomplete to `reboot.py target`  
`-i` regenerate initrd (for now only using dracut)  
`-g` regenerates grub config  
`-y` doesnt ask before rebooting  

#### todo
default behavior for target  
detect tool used for initrd  
make it drop replacment for 'reboot'  
handle not existing config

