import {
  LMap,
  LTileLayer,
  LMarker,
  LCircleMarker,
  LPopup,
  LIcon,
} from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.component("LMap", LMap);
  nuxtApp.vueApp.component("LTileLayer", LTileLayer);
  nuxtApp.vueApp.component("LMarker", LMarker);
  nuxtApp.vueApp.component("LCircleMarker", LCircleMarker);
  nuxtApp.vueApp.component("LPopup", LPopup);
  nuxtApp.vueApp.component("LIcon", LIcon);
});
