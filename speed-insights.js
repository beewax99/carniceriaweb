// Initialize Vercel Speed Insights
// This module imports and configures Speed Insights for the static HTML site
import { injectSpeedInsights } from '@vercel/speed-insights';

// Inject Speed Insights with configuration
injectSpeedInsights({
  debug: true, // Enable debug logging in development
});
