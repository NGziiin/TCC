// Modules to control application life and create native browser window
const { app, BrowserWindow, screen } = require('electron')
const path = require('node:path')
require('electron-reload')(__dirname, {
  electron: require(`${__dirname}/node_modules/electron`)
})

let mainWindow = null

app.whenReady().then(() => {
  const primaryDisplay = screen.getPrimaryDisplay()
  const { width, height } = primaryDisplay.workAreaSize

  mainWindow = new BrowserWindow({
    width,
    height,
    resizable: true,
    maximizable: true,
    fullscreenable: false,
    autoHideMenuBar: true,

    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      sandbox: false
    }})

  mainWindow.maximize();
  mainWindow.loadFile('../gui/login/login.html')
  mainWindow.webContents.openDevTools(); // remover no final do software

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})

