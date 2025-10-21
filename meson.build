project(
    'mauna-power-manager',
    meson_version: '>= 0.49.0',
    version : '2.0',
    license: ['GplV3']
)

subdir('po')

libexec_dir = '/usr/libexec/'
bin_dir = '/usr/bin/'

mauna_dir = '/usr/share/mauna/power-manager/'
icons_dir = '/usr/share/icons/hicolor/scalable/status/'
app_icon_dir = '/usr/share/icons/hicolor/scalable/apps/'
udev_dir = '/lib/udev/rules.d'
application_dir = '/usr/share/applications/'
policy_dir = '/usr/share/polkit-1/actions/'
autostart_dir = '/etc/xdg/autostart/'

# install source code
install_subdir('src/client', install_dir: mauna_dir)
install_subdir('src/service', install_dir: mauna_dir)
install_subdir('src/common', install_dir: mauna_dir)
install_subdir('src/udev-trigger', install_dir: mauna_dir)
install_subdir('src/data', install_dir: mauna_dir)
# install icons
foreach icon : ['mpm-performance-button', 'mpm-balanced-button', 'mpm-powersave-button', 
                'mauna-pm-performance-symbolic', 'mauna-pm-powersave-symbolic',
                'mauna-pm-balanced-symbolic']
    install_data('data/'+icon+'.svg', install_dir: icons_dir)
endforeach
install_data('data/mauna-power-manager.svg', install_dir: app_icon_dir)
# install desktop files
install_data('data/mpm-client.desktop', install_dir: application_dir, rename: 'top.mauna.power-manager.desktop')
meson.add_install_script('sh', '-c',
    'ln -s ../share/mauna/power-manager/client/main.py ' +
    '${DESTDIR}/' + bin_dir + '/mauna-power-manager')
install_data('data/mpm-autostart.desktop', install_dir: autostart_dir)
# install policy file
install_data('data/mpm.policy', install_dir: libexec_dir, rename: 'top.mauna.pkexec.mauna-power-manager.policy')
install_data('src/udev-trigger/mpm.rule', install_dir: udev_dir, rename: '99-mpm.rules')
# install scripts
install_data('data/mpm-libexec.sh', install_dir: libexec_dir, rename: 'mauna-power-manager')
install_data('data/mpm-cli.sh', install_dir: bin_dir, rename: 'mpm')
install_data('data/mpm-trigger.sh', install_dir: libexec_dir, rename: 'mpm-trigger')

if get_option('service') == 'systemd'
    install_data('data/mpm.systemd', install_dir: '/lib/systemd/system/', rename: 'mpm.service')
elif get_option('service') == 'openrc'
    install_data('data/mpm.openrc', install_dir: '/etc/init.d/', rename: 'mpm')
elif get_option('service') == 'sysvinit'
    install_data('data/mpm.sysvinit', install_dir: '/etc/init.d/', rename: 'mpm')
endif
