import { onRequestPost as __api_login_js_onRequestPost } from "C:\\Users\\Admin\\Desktop\\discordbot\\vite-mantine\\functions\\api\\login.js"
import { onRequestPost as __api_register_js_onRequestPost } from "C:\\Users\\Admin\\Desktop\\discordbot\\vite-mantine\\functions\\api\\register.js"

export const routes = [
    {
      routePath: "/api/login",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_login_js_onRequestPost],
    },
  {
      routePath: "/api/register",
      mountPath: "/api",
      method: "POST",
      middlewares: [],
      modules: [__api_register_js_onRequestPost],
    },
  ]