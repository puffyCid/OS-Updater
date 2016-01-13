import xbmcaddon
import xbmcgui
import xbmc
import subprocess
import sys
import time

ACTION_PREVIOUS_MENU = 10

'''
Method/Function to upgrade the operating system.  Executes upgrade commands based on addon setting. Ex: apt-get
'''
def UniversalUpdater(password, updateCommandY):
        addon = xbmcaddon.Addon()
        addonName = addon.getAddonInfo('name')
        output = subprocess.Popen(["echo " + password + " | sudo -S " + updateCommandY], shell=True)
        updateProgress = xbmcgui.DialogProgress()
        updateProgress.create("Kodi", addon.getLocalizedString(32006))
        if(updateProgress.iscanceled()):
            sys.exit() 
        output.wait()
        updateProgress.close()
        xbmcgui.Dialog().ok(addonName, addon.getLocalizedString(32005))
'''
Method/Function to fetch updates.  Executes update commands based on addon setting. Ex: apt-get.
Checks if user entered password correctly based on update output response.
Returns a string of updates.

If string length is less than 2, informs the user that they likely inputed an incorrect password
'''
def FetchUpdates(password, updateCommand):
        addon = xbmcaddon.Addon()
        addonName = addon.getAddonInfo('name')
        output = subprocess.Popen(["echo " + password + " | sudo -S " + updateCommand], stdout=subprocess.PIPE, shell=True)
        fetchUpdates = xbmcgui.DialogProgress()
        fetchUpdates.create("Kodi", addon.getLocalizedString(32003))
        if(fetchUpdates.iscanceled()):
            sys.exit()
        output.wait()
        fetchUpdates.close()
        output = output.communicate()[0]
        if(len(output) < 2):
            xbmcgui.Dialog().ok(addonName, addon.getLocalizedString(32002))
            sys.exit()
        return output
'''
XBMC window class.
Prompts user for their sudo password.  Used to upgrade OS.
Based on addon setting selects correct upgrade command Ex: apt-get
Executes a XBMC built in full screen window, display's label, and display's updates
If user wants to update, proceeds to upgrade the OS
'''
class UpdateWindow(xbmcgui.Window):
    def onAction(self, action):
        if(action == ACTION_PREVIOUS_MENU):
            self.close()
    addon = xbmcaddon.Addon()
    addonName = addon.getAddonInfo('name')
    output = ""
    inputText = xbmc.Keyboard('', addon.getLocalizedString(32007), True)
    inputText.doModal()
    if(inputText.isConfirmed()):
        text = "\'" + inputText.getText() + "\'"
        
    if(addon.getSetting('RedHat') == 'true'):
        updateFedora = "dnf update --assumeno"
        output = FetchUpdates(text, updateFedora)
    
    if(addon.getSetting('Debian') == 'true'):  
        updateDebian = "apt-get update -qq && echo " + text + " | sudo -S apt-get upgrade -V --assume-no"
        output = FetchUpdates(text, updateDebian)
        
    if(addon.getSetting('Arch') == 'true'):    
        updateArch = "pacman -Syu"
        output = FetchUpdates(text, updateArch)
    
    if(addon.getSetting('ArchAur') == 'true'):    
        updateArchAur = "yaourt -Syu"
        output = FetchUpdates(text, updateArchAur)

    xbmc.executebuiltin("ActivateWindow(%d)" % 10147)
    window = xbmcgui.Window(10147)
    time.sleep(5)
    window.getControl(1).setLabel(addon.getLocalizedString(32005))
    window.getControl(5).setText(output)
    
    answer = xbmcgui.Dialog().yesno(addonName, addon.getLocalizedString(32004))
    if(answer == True):
        # inputText = xbmc.Keyboard('', 'Enter password', True)
        # inputText.doModal()
        # if(inputText.isConfirmed()):
            # text = "\'" + inputText.getText() + "\'"  
                  
        if(addon.getSetting('RedHat') == 'true'):       
            updateFedoraY = "dnf -y update"
            
            UniversalUpdater(text, updateFedoraY)
            
        if(addon.getSetting('Debian') == 'true'):  
            updateDebianY = "apt-get -y upgrade"
            
            UniversalUpdater(text, updateDebianY)
             
        if(addon.getSetting('Arch') == 'true'):    
            updateArchY = "pacman -Syu --noconfirm"
            
            UniversalUpdater(text, updateArchY)
            
        if(addon.getSetting('ArchAur') == 'true'):    
            updateArchAurY = "yaourt -Syu --noconfirm"
            
            UniversalUpdater(text, updateArchAurY)
    
updater = UpdateWindow()
updater.doModal()
del updater