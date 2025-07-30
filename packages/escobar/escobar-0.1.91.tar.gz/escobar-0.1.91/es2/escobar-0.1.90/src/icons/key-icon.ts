// Import the LabIcon class from JupyterLab UI components
import { LabIcon } from '@jupyterlab/ui-components';

// Define the SVG string for the key icon (vertical orientation)
const keySvgStr = `
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="6" r="3"/>
  <path d="M12 9v12"/>
  <path d="M15 18h3"/>
  <path d="M15 15h2"/>
</svg>
`;

// Export the key icon
export const keyIcon = new LabIcon({
  name: 'escobar:key-icon',
  svgstr: keySvgStr
});
