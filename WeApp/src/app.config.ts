export default {
  pages: [
    "pages/index/index",
    "pages/game/game",
    "pages/rank/rank"
    
  ],
  window: {
    backgroundTextStyle: 'light',
    navigationBarBackgroundColor: '#405f80',
    navigationBarTitleText: '配音大师',
    navigationBarTextStyle: 'black'
  },
  tabBar: {
    color: "#000000",
    selectedColor: "#ff9900",
    backgroundColor: "#ffffff",
    borderStyle: "white",
    list: [{
        "pagePath": "pages/game/game",
        "text": "游 戏",
        "iconPath": "./static/game.png",
        "selectedIconPath": "./static/game.png",
      },{
        "pagePath": "pages/rank/rank",
        "text": "排 名",
        "iconPath": "./static/rank.png",
        "selectedIconPath": "./static/rank.png",
      }],
  },

}
