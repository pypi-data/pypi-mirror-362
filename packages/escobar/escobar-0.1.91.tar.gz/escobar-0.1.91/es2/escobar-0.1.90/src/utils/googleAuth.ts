/**
 * Google OAuth Authentication Manager
 * Handles Google OAuth flow using popup windows for non-disruptive authentication
 */

export interface IGoogleAuthConfig {
    clientId: string;
    redirectUri?: string;
    scope?: string;
}

export interface IGoogleAuthResult {
    success: boolean;
    idToken?: string;
    accessToken?: string;
    error?: string;
    userInfo?: {
        email: string;
        name: string;
        picture?: string;
    };
}

export class GoogleAuthManager {
    private clientId: string;
    private scope: string;
    private redirectUri: string;
    private currentToken: string | null = null;
    private userInfo: any = null;

    constructor(config: IGoogleAuthConfig) {
        this.clientId = config.clientId;
        this.scope = config.scope || 'openid email profile';
        this.redirectUri = config.redirectUri || `${window.location.origin}/oauth/callback`;
    }

    /**
     * Initiate Google OAuth login using popup window
     */
    async login(): Promise<IGoogleAuthResult> {
        return new Promise((resolve) => {
            // Create OAuth URL
            const authUrl = this.buildAuthUrl();

            // Open popup window
            const popup = window.open(
                authUrl,
                'google-oauth',
                'width=500,height=600,scrollbars=yes,resizable=yes'
            );

            if (!popup) {
                resolve({
                    success: false,
                    error: 'Failed to open popup window. Please allow popups for this site.'
                });
                return;
            }

            // Listen for popup messages
            const messageListener = (event: MessageEvent) => {
                // Verify origin for security
                if (event.origin !== window.location.origin) {
                    return;
                }

                if (event.data.type === 'GOOGLE_OAUTH_SUCCESS') {
                    window.removeEventListener('message', messageListener);
                    popup.close();

                    this.currentToken = event.data.idToken;
                    this.userInfo = event.data.userInfo;

                    resolve({
                        success: true,
                        idToken: event.data.idToken,
                        accessToken: event.data.accessToken,
                        userInfo: event.data.userInfo
                    });
                } else if (event.data.type === 'GOOGLE_OAUTH_ERROR') {
                    window.removeEventListener('message', messageListener);
                    popup.close();

                    resolve({
                        success: false,
                        error: event.data.error
                    });
                }
            };

            window.addEventListener('message', messageListener);

            // Check if popup was closed manually
            const checkClosed = setInterval(() => {
                if (popup.closed) {
                    clearInterval(checkClosed);
                    window.removeEventListener('message', messageListener);
                    resolve({
                        success: false,
                        error: 'Authentication cancelled by user'
                    });
                }
            }, 1000);
        });
    }

    /**
     * Google Identity Services (GSI) login method
     * This uses Google's official Identity Services library for secure authentication
     * Now uses popup-only approach without One Tap UI
     */
    async loginWithGSI(): Promise<IGoogleAuthResult> {
        return new Promise((resolve) => {
            try {
                // Load Google Identity Services if not already loaded
                this.loadGoogleIdentityServices().then(() => {
                    console.log('Google Identity Services loaded, initializing popup authentication...');

                    // Initialize Google Identity Services for popup-only authentication
                    (window as any).google.accounts.id.initialize({
                        client_id: this.clientId,
                        callback: (response: any) => {
                            console.log('Google authentication callback triggered');

                            if (response.credential) {
                                // Decode the JWT token to get user info
                                const userInfo = this.decodeJWT(response.credential);
                                this.currentToken = response.credential;
                                this.userInfo = userInfo;

                                // Comprehensive token logging
                                console.log('=== GOOGLE AUTHENTICATION SUCCESS ===');
                                console.log('ID Token:', response.credential);
                                console.log('Access Token:', response.access_token || 'Not provided');
                                console.log('Decoded JWT Payload:', userInfo);
                                console.log('User Info:', {
                                    email: userInfo.email,
                                    name: userInfo.name,
                                    picture: userInfo.picture
                                });
                                console.log('Token Expiration:', userInfo.exp ? new Date(userInfo.exp * 1000) : 'Not specified');
                                console.log('Token Issued At:', userInfo.iat ? new Date(userInfo.iat * 1000) : 'Not specified');
                                console.log('=====================================');

                                resolve({
                                    success: true,
                                    idToken: response.credential,
                                    accessToken: response.access_token,
                                    userInfo: {
                                        email: userInfo.email,
                                        name: userInfo.name,
                                        picture: userInfo.picture
                                    }
                                });
                            } else {
                                console.error('No credential received from Google authentication');
                                resolve({
                                    success: false,
                                    error: 'No credential received from Google'
                                });
                            }
                        },
                        auto_select: false,
                        cancel_on_tap_outside: true,
                        use_fedcm_for_prompt: true // Enable FedCM compatibility
                    });

                    // Skip One Tap entirely and go directly to popup authentication
                    console.log('Triggering Google popup authentication...');
                    this.triggerPopupAuthentication(resolve);

                }).catch((error) => {
                    console.error('Failed to load Google Identity Services:', error);
                    resolve({
                        success: false,
                        error: `Failed to load Google Identity Services: ${error.message}`
                    });
                });

            } catch (error) {
                console.error('Google Sign-In error:', error);
                resolve({
                    success: false,
                    error: `Google Sign-In error: ${error.message}`
                });
            }
        });
    }

    /**
     * Trigger popup-based Google authentication using GSI renderButton
     */
    private triggerPopupAuthentication(resolve: (result: IGoogleAuthResult) => void): void {
        try {
            console.log('Creating temporary Google Sign-In button for popup authentication...');

            // Create a temporary invisible container for the Google Sign-In button
            const tempContainer = document.createElement('div');
            tempContainer.id = 'google-signin-temp-container';
            tempContainer.style.position = 'fixed';
            tempContainer.style.top = '-1000px'; // Hide it off-screen
            tempContainer.style.left = '-1000px';
            tempContainer.style.width = '1px';
            tempContainer.style.height = '1px';
            tempContainer.style.overflow = 'hidden';
            tempContainer.style.opacity = '0';
            tempContainer.style.pointerEvents = 'none';

            document.body.appendChild(tempContainer);

            // Render the Google Sign-In button in the hidden container
            (window as any).google.accounts.id.renderButton(tempContainer, {
                theme: 'outline',
                size: 'large',
                type: 'standard',
                shape: 'rectangular',
                text: 'signin_with',
                logo_alignment: 'left'
            });

            // Find the rendered button and trigger a click programmatically
            setTimeout(() => {
                const renderedButton = tempContainer.querySelector('div[role="button"]') as HTMLElement;
                if (renderedButton) {
                    console.log('Triggering Google Sign-In button click...');
                    renderedButton.click();
                } else {
                    console.error('Could not find rendered Google Sign-In button');
                    document.body.removeChild(tempContainer);
                    resolve({
                        success: false,
                        error: 'Failed to trigger Google Sign-In button'
                    });
                }
            }, 500);

            // Clean up the temporary container after a delay
            setTimeout(() => {
                if (document.body.contains(tempContainer)) {
                    document.body.removeChild(tempContainer);
                }
            }, 5000);

        } catch (error) {
            console.error('Error triggering popup authentication:', error);
            resolve({
                success: false,
                error: `Popup authentication error: ${error.message}`
            });
        }
    }

    /**
     * Build Google OAuth URL for popup authentication
     */
    private buildGoogleAuthUrl(): string {
        const params = new URLSearchParams({
            client_id: this.clientId,
            redirect_uri: this.redirectUri,
            response_type: 'code',
            scope: this.scope,
            access_type: 'offline',
            prompt: 'select_account',
            state: this.generateState()
        });

        return `https://accounts.google.com/oauth/authorize?${params.toString()}`;
    }


    /**
     * Load Google Identity Services library dynamically
     */
    private loadGoogleIdentityServices(): Promise<void> {
        return new Promise((resolve, reject) => {
            // Check if already loaded
            if (typeof (window as any).google !== 'undefined' &&
                (window as any).google.accounts &&
                (window as any).google.accounts.id) {
                resolve();
                return;
            }

            // Create script element
            const script = document.createElement('script');
            script.src = 'https://accounts.google.com/gsi/client';
            script.async = true;
            script.defer = true;

            script.onload = () => {
                // Wait a bit for the library to initialize
                setTimeout(() => {
                    if (typeof (window as any).google !== 'undefined' &&
                        (window as any).google.accounts &&
                        (window as any).google.accounts.id) {
                        resolve();
                    } else {
                        reject(new Error('Google Identity Services failed to initialize'));
                    }
                }, 100);
            };

            script.onerror = () => {
                reject(new Error('Failed to load Google Identity Services script'));
            };

            // Add to document head
            document.head.appendChild(script);
        });
    }

    /**
     * Generate a random nonce for security
     */
    private generateNonce(): string {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }

    /**
     * Generate a random state for security
     */
    private generateState(): string {
        return Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
    }

    /**
     * Build OAuth authorization URL
     */
    private buildAuthUrl(): string {
        const params = new URLSearchParams({
            client_id: this.clientId,
            redirect_uri: this.redirectUri,
            response_type: 'code',
            scope: this.scope,
            access_type: 'offline',
            prompt: 'consent'
        });

        return `https://accounts.google.com/oauth/authorize?${params.toString()}`;
    }

    /**
     * Decode JWT token to extract user information
     */
    private decodeJWT(token: string): any {
        try {
            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64)
                    .split('')
                    .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                    .join('')
            );
            return JSON.parse(jsonPayload);
        } catch (error) {
            console.error('Error decoding JWT:', error);
            return {};
        }
    }

    /**
     * Get current authentication status
     */
    isAuthenticated(): boolean {
        return this.currentToken !== null;
    }

    /**
     * Get current ID token
     */
    getIdToken(): string | null {
        return this.currentToken;
    }

    /**
     * Get current user info
     */
    getUserInfo(): any {
        return this.userInfo;
    }

    /**
     * Logout and clear stored tokens
     */
    logout(): void {
        this.currentToken = null;
        this.userInfo = null;

        // Also revoke Google session if possible
        if (typeof (window as any).google !== 'undefined') {
            try {
                (window as any).google.accounts.id.disableAutoSelect();
            } catch (error) {
                console.warn('Error disabling Google auto-select:', error);
            }
        }
    }

    /**
     * Validate token (basic check)
     */
    validateToken(): boolean {
        if (!this.currentToken) {
            return false;
        }

        try {
            const decoded = this.decodeJWT(this.currentToken);
            const now = Math.floor(Date.now() / 1000);

            // Check if token is expired
            if (decoded.exp && decoded.exp < now) {
                this.logout();
                return false;
            }

            return true;
        } catch (error) {
            console.error('Error validating token:', error);
            this.logout();
            return false;
        }
    }
}

// Global instance for easy access
let globalAuthManager: GoogleAuthManager | null = null;

/**
 * Initialize global Google Auth manager
 */
export function initializeGoogleAuth(config: IGoogleAuthConfig): GoogleAuthManager {
    globalAuthManager = new GoogleAuthManager(config);
    return globalAuthManager;
}

/**
 * Get global Google Auth manager instance
 */
export function getGoogleAuthManager(): GoogleAuthManager | null {
    return globalAuthManager;
}
