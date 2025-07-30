// Import the LabIcon class from JupyterLab UI components
import { LabIcon } from '@jupyterlab/ui-components';

// Define the SVG string for the key icon (fatter, more prominent design)
const keySvgStr = `
<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="7" r="4"/>
  <path d="M12 11v10"/>
  <path d="M14 19h4"/>
  <path d="M14 16h3"/>
  <path d="M14 22h2"/>
</svg>
`;

// Export the key icon
export const keyIcon = new LabIcon({
  name: 'escobar:key-icon',
  svgstr: keySvgStr
});
