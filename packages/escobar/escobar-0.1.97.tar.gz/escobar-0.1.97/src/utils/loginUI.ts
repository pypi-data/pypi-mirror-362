import { getGoogleAuthManager, initializeGoogleAuth, IGoogleAuthResult } from './googleAuth';

/**
 * Interface for authentication provider options
 */
export interface IAuthProvider {
    id: string;
    name: string;
    icon: string;
    description: string;
}

/**
 * Enhanced Login UI class with better error handling and user experience
 */
export class LoginUI {
    private overlay: HTMLDivElement;
    private container: HTMLDivElement;
    private onSuccess: (apiKey: string) => void;
    private onCancel: () => void;

    // Available authentication providers
    private authProviders: IAuthProvider[] = [
        {
            id: 'google',
            name: 'Google',
            icon: '<svg viewBox="0 0 24 24" width="18" height="18"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>',
            description: 'Sign in with your Google account'
        }
    ];

    /**
     * Create a new LoginUI
     * @param onSuccess Callback when authentication is successful
     * @param onCancel Callback when authentication is cancelled
     */
    constructor(
        onSuccess: (apiKey: string) => void,
        onCancel: () => void
    ) {
        this.onSuccess = onSuccess;
        this.onCancel = onCancel;

        // Create overlay
        this.overlay = document.createElement('div');
        this.overlay.className = 'escobar-login-overlay';
        this.overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 10000;
            opacity: 0;
            transition: opacity 0.3s ease;
        `;

        this.overlay.addEventListener('click', (e) => {
            if (e.target === this.overlay) {
                this.hide();
                this.onCancel();
            }
        });

        // Create container
        this.container = this.createContainer();
        this.overlay.appendChild(this.container);
    }

    /**
     * Create the login UI container with enhanced styling
     */
    private createContainer(): HTMLDivElement {
        const container = document.createElement('div');
        container.className = 'escobar-login-container';
        container.style.cssText = `
            background: var(--jp-layout-color0);
            border: 1px solid var(--jp-border-color1);
            border-radius: 8px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            transform: scale(0.9);
            transition: transform 0.3s ease;
        `;

        // Create header
        const header = document.createElement('div');
        header.style.cssText = `
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 24px 16px;
            border-bottom: 1px solid var(--jp-border-color1);
        `;

        const title = document.createElement('h2');
        title.textContent = 'Authentication Required';
        title.style.cssText = `
            margin: 0;
            color: var(--jp-content-font-color1);
            font-size: 18px;
            font-weight: 600;
        `;
        header.appendChild(title);

        const closeButton = document.createElement('button');
        closeButton.innerHTML = '&times;';
        closeButton.style.cssText = `
            background: none;
            border: none;
            font-size: 24px;
            color: var(--jp-content-font-color2);
            cursor: pointer;
            padding: 0;
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: background-color 0.2s ease;
        `;
        closeButton.addEventListener('click', () => {
            this.hide();
            this.onCancel();
        });
        closeButton.addEventListener('mouseenter', () => {
            closeButton.style.backgroundColor = 'var(--jp-layout-color2)';
        });
        closeButton.addEventListener('mouseleave', () => {
            closeButton.style.backgroundColor = 'transparent';
        });
        header.appendChild(closeButton);

        container.appendChild(header);

        // Create content
        const content = document.createElement('div');
        content.style.cssText = `
            padding: 24px;
        `;

        // Add description
        const description = document.createElement('p');
        description.textContent = 'Please authenticate to access AI services:';
        description.style.cssText = `
            margin: 0 0 20px 0;
            color: var(--jp-content-font-color2);
            font-size: 14px;
            line-height: 1.5;
        `;
        content.appendChild(description);

        // Add auth providers
        const providersList = document.createElement('div');
        providersList.style.cssText = `
            display: flex;
            flex-direction: column;
            gap: 12px;
        `;

        this.authProviders.forEach(provider => {
            const providerButton = document.createElement('button');
            providerButton.dataset.provider = provider.id;
            providerButton.style.cssText = `
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 16px;
                background: var(--jp-layout-color1);
                border: 1px solid var(--jp-border-color1);
                border-radius: 6px;
                cursor: pointer;
                transition: all 0.2s ease;
                text-align: left;
                width: 100%;
            `;

            // Hover effects
            providerButton.addEventListener('mouseenter', () => {
                providerButton.style.backgroundColor = 'var(--jp-layout-color2)';
                providerButton.style.borderColor = 'var(--jp-brand-color1)';
            });
            providerButton.addEventListener('mouseleave', () => {
                providerButton.style.backgroundColor = 'var(--jp-layout-color1)';
                providerButton.style.borderColor = 'var(--jp-border-color1)';
            });

            const providerIcon = document.createElement('span');
            providerIcon.innerHTML = provider.icon;
            providerIcon.style.cssText = `
                flex-shrink: 0;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            providerButton.appendChild(providerIcon);

            const providerInfo = document.createElement('div');
            providerInfo.style.cssText = `
                flex: 1;
            `;

            const providerName = document.createElement('div');
            providerName.textContent = provider.name;
            providerName.style.cssText = `
                font-weight: 500;
                color: var(--jp-content-font-color1);
                font-size: 14px;
                margin-bottom: 2px;
            `;
            providerInfo.appendChild(providerName);

            const providerDesc = document.createElement('div');
            providerDesc.textContent = provider.description;
            providerDesc.style.cssText = `
                font-size: 12px;
                color: var(--jp-content-font-color2);
                line-height: 1.3;
            `;
            providerInfo.appendChild(providerDesc);

            providerButton.appendChild(providerInfo);

            // Add click handler
            providerButton.addEventListener('click', () => {
                this.handleProviderClick(provider.id);
            });

            providersList.appendChild(providerButton);
        });

        content.appendChild(providersList);
        container.appendChild(content);

        return container;
    }

    /**
     * Enhanced provider click handler with better error handling
     */
    private async handleProviderClick(providerId: string): Promise<void> {
        if (providerId === 'google') {
            // Show loading state
            this.setLoadingState(providerId, true);

            try {
                // Get or initialize Google auth manager
                let authManager = getGoogleAuthManager();
                if (!authManager) {
                    // Get Google Client ID from settings
                    const currentSettings = (window as any).escobarCurrentSettings;
                    const googleClientId = currentSettings?.googleClientId;

                    if (!googleClientId) {
                        this.setLoadingState(providerId, false);
                        this.showError('Google Client ID not configured. Please set it in the settings first.');
                        return;
                    }

                    authManager = initializeGoogleAuth({
                        clientId: googleClientId,
                        scope: 'openid email profile https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/documents.readonly'
                    });
                }

                // Attempt Google authentication
                const result: IGoogleAuthResult = await authManager.loginWithAuthCode();

                this.setLoadingState(providerId, false);

                if (result.success && result.idToken) {
                    console.log('🔐 LOGIN-UI: Authentication successful');

                    // Store tokens globally for backend communication
                    (window as any).escobarGoogleIdToken = result.idToken;
                    (window as any).escobarGoogleUserInfo = result.userInfo;

                    // Hide the login UI and return the ID token
                    this.hide();
                    this.onSuccess(result.idToken);
                } else {
                    console.error('🔐 LOGIN-UI: Authentication failed:', result.error);
                    this.showError(result.error || 'Authentication failed. Please try again.');
                }
            } catch (error) {
                console.error('🔐 LOGIN-UI: Authentication error:', error);
                this.setLoadingState(providerId, false);
                this.showError(`Authentication error: ${error.message || 'Unknown error occurred'}`);
            }
        } else {
            // For other providers, show not implemented message
            this.showError(`${this.getProviderById(providerId).name} authentication is not yet implemented.`);
        }
    }

    /**
     * Set loading state for a provider button
     */
    private setLoadingState(providerId: string, isLoading: boolean): void {
        const button = this.container.querySelector(`button[data-provider="${providerId}"]`) as HTMLButtonElement;
        if (!button) return;

        if (isLoading) {
            button.disabled = true;
            button.style.opacity = '0.6';
            button.style.cursor = 'not-allowed';

            const providerName = button.querySelector('div > div:first-child');
            if (providerName) {
                providerName.textContent = `Connecting to ${this.getProviderById(providerId).name}...`;
            }
        } else {
            button.disabled = false;
            button.style.opacity = '1';
            button.style.cursor = 'pointer';

            const providerName = button.querySelector('div > div:first-child');
            if (providerName) {
                providerName.textContent = this.getProviderById(providerId).name;
            }
        }
    }

    /**
     * Show error message to user
     */
    private showError(message: string): void {
        // Remove any existing error messages
        const existingError = this.container.querySelector('.escobar-login-error');
        if (existingError) {
            existingError.remove();
        }

        // Create error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'escobar-login-error';
        errorDiv.textContent = message;
        errorDiv.style.cssText = `
            background: var(--jp-error-color3);
            color: var(--jp-error-color1);
            border: 1px solid var(--jp-error-color1);
            border-radius: 4px;
            padding: 12px;
            margin: 16px 24px;
            font-size: 13px;
            line-height: 1.4;
        `;

        // Insert before the content
        const content = this.container.querySelector('div:last-child');
        if (content) {
            this.container.insertBefore(errorDiv, content);
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (errorDiv.parentNode) {
                errorDiv.parentNode.removeChild(errorDiv);
            }
        }, 5000);
    }

    /**
     * Get provider by ID
     */
    private getProviderById(id: string): IAuthProvider {
        return this.authProviders.find(p => p.id === id) || this.authProviders[0];
    }

    /**
     * Show the login UI with animation
     */
    public show(): void {
        document.body.appendChild(this.overlay);

        // Trigger animation
        requestAnimationFrame(() => {
            this.overlay.style.opacity = '1';
            this.container.style.transform = 'scale(1)';
        });
    }

    /**
     * Hide the login UI with animation
     */
    public hide(): void {
        this.overlay.style.opacity = '0';
        this.container.style.transform = 'scale(0.9)';

        // Remove from DOM after animation
        setTimeout(() => {
            if (this.overlay.parentNode) {
                this.overlay.parentNode.removeChild(this.overlay);
            }
        }, 300);
    }
}

/**
 * Show the enhanced login UI and return a promise that resolves with the API key
 */
export function showLoginUI(): Promise<string> {
    return new Promise((resolve, reject) => {
        const loginUI = new LoginUI(
            // Success callback
            (apiKey) => {
                resolve(apiKey);
            },
            // Cancel callback
            () => {
                reject(new Error('Authentication cancelled'));
            }
        );
        loginUI.show();
    });
}
