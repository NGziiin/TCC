// Modules to control application life and create native browser window
const { app, BrowserWindow, screen } = require('electron')
const path = require('node:path')

let mainWindow = null

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize

  require(path.join(__dirname, 'backend', 'StartingSystem.js'))

  mainWindow = new BrowserWindow({
    width,
    height,
    resizable: true,
    maximizable: true,
    fullscreenable: false,
    autoHideMenuBar: true,

    webPreferences: {
      preload: path.join(__dirname, 'preload.js')
    }})

  mainWindow.maximize();
  mainWindow.loadFile('../gui/login/login.html')

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

