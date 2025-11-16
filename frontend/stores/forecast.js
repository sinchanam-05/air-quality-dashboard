import { defineStore } from "pinia";
import axios from "axios";

export const useForecastStore = defineStore("forecast", () => {
  // Use Nuxt's composable for configuration
  const config = useRuntimeConfig();
  const apiBase = config.public.apiBase;

  // --- State ---
  const currentLatitude = ref(37.7749); // Default: San Francisco
  const currentLongitude = ref(-122.4194); // Default: San Francisco
  const forecastData = ref(null); // Holds the entire HyperLocalForecast object from the backend
  const activeHourIndex = ref(0); // 0 to 71, controlled by the time slider
  const loading = ref(false);
  const error = ref(null);

  // --- Getters (Computed Properties) ---

  // Get the specific data point for the currently selected hour
  const activeDataPoint = computed(() => {
    if (!forecastData.value) return null;

    const index = activeHourIndex.value;

    return {
      aqi: forecastData.value.air_quality_series[index],
      allergen: forecastData.value.allergen_series[index],
    };
  });

  // Get the map center based on the forecast point (not the requested point)
  const mapCenter = computed(() => {
    if (!forecastData.value)
      return [currentLatitude.value, currentLongitude.value];
    return [forecastData.value.latitude, forecastData.value.longitude];
  });

  // --- Actions (Methods) ---

  /**
   * Fetches the 72-hour forecast from the FastAPI backend.
   * @param {float} lat - Target latitude
   * @param {float} lon - Target longitude
   */
  async function fetchForecast(lat, lon) {
    loading.value = true;
    error.value = null;

    // Update the state to reflect the new requested location
    currentLatitude.value = lat;
    currentLongitude.value = lon;

    try {
      const response = await axios.get(`${apiBase}/forecast/${lat}/${lon}`);
      forecastData.value = response.data;

      // Reset slider to the start of the forecast upon new data load
      activeHourIndex.value = 0;
    } catch (err) {
      console.error("API Fetch Error:", err);
      error.value = "Failed to load forecast data. Check backend connection.";
      forecastData.value = null;
    } finally {
      loading.value = false;
    }
  }

  return {
    // State
    currentLatitude,
    currentLongitude,
    forecastData,
    activeHourIndex,
    loading,
    error,

    // Getters
    activeDataPoint,
    mapCenter,

    // Actions
    fetchForecast,
  };
});
