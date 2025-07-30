/**
 * Enhanced Google OAuth Authentication Manager
 * Handles Google OAuth flow using popup windows for non-disruptive authentication
 * Includes improvements for error handling, security, and user experience
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
    authorizationCode?: string;
    redirectUri?: string;
    state?: string;
    error?: string;
    userInfo?: {
        email: string;
        name: string;
        picture?: string;
    };
}

export interface IGoogleUserInfo {
    email: string;
    name: string;
    picture?: string;
    sub: string;
    iss: string;
    aud: string;
    exp: number;
    iat: number;
}

export class GoogleAuthManager {
    private clientId: string;
    private scope: string;
    private redirectUri: string;
    private currentToken: string | null = null;
    private userInfo: IGoogleUserInfo | null = null;
    private tokenExpirationTime: number | null = null;

    constructor(config: IGoogleAuthConfig) {
        this.clientId = config.clientId;
        this.scope = config.scope || 'openid email profile https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/documents.readonly';
        this.redirectUri = config.redirectUri || `${window.location.origin}/escobar/oauth-callback.html`;

        // Validate client ID format
        if (!this.isValidClientId(this.clientId)) {
            console.warn('Invalid Google Client ID format. Please check your configuration.');
        }
    }

    /**
     * Validate Google Client ID format
     */
    private isValidClientId(clientId: string): boolean {
        return clientId && clientId.includes('.apps.googleusercontent.com');
    }

    /**
     * OAuth 2.0 Authorization Code Flow
     * Opens popup to Google OAuth endpoint and returns authorization code
     */
    async loginWithAuthCode(): Promise<IGoogleAuthResult> {
        return new Promise((resolve) => {
            try {
                // Validate client ID before proceeding
                if (!this.isValidClientId(this.clientId)) {
                    resolve({
                        success: false,
                        error: 'Invalid Google Client ID. Please configure a valid Client ID in settings.'
                    });
                    return;
                }

                console.log('🔐 AUTH: Starting OAuth authorization code flow with Client ID:', this.clientId.substring(0, 20) + '...');

                // Generate state parameter for security
                const state = this.generateRandomState();

                // Build OAuth URL
                const oauthUrl = this.buildOAuthUrl(state);
                console.log('🔐 AUTH: Opening OAuth popup to:', oauthUrl);

                // Open popup window
                const popup = window.open(
                    oauthUrl,
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

                // Set up message listener for OAuth callback
                const messageListener = (event: MessageEvent) => {
                    // Verify origin for security
                    if (event.origin !== window.location.origin) {
                        console.warn('🔐 AUTH: Ignoring message from unknown origin:', event.origin);
                        return;
                    }

                    if (event.data.type === 'GOOGLE_OAUTH_CODE_SUCCESS') {
                        console.log('🔐 AUTH: Authorization code received successfully');

                        // Verify state parameter
                        if (event.data.state !== state) {
                            console.error('🔐 AUTH: State parameter mismatch');
                            resolve({
                                success: false,
                                error: 'Security validation failed (state mismatch)'
                            });
                            cleanup();
                            return;
                        }

                        // Store the authorization code
                        const authCode = event.data.authorizationCode;
                        console.log('🔐 AUTH: Authorization code:', authCode.substring(0, 20) + '...');

                        resolve({
                            success: true,
                            authorizationCode: authCode,
                            redirectUri: this.redirectUri,
                            state: state
                        });
                        cleanup();

                    } else if (event.data.type === 'GOOGLE_OAUTH_CODE_ERROR') {
                        console.error('🔐 AUTH: OAuth error:', event.data.error);
                        resolve({
                            success: false,
                            error: event.data.error || 'OAuth authentication failed'
                        });
                        cleanup();
                    }
                };

                // Cleanup function
                const cleanup = () => {
                    window.removeEventListener('message', messageListener);
                    if (popup && !popup.closed) {
                        popup.close();
                    }
                };

                // Add message listener
                window.addEventListener('message', messageListener);

                // Check if popup was closed manually
                const checkClosed = setInterval(() => {
                    if (popup.closed) {
                        clearInterval(checkClosed);
                        resolve({
                            success: false,
                            error: 'Authentication cancelled by user'
                        });
                        cleanup();
                    }
                }, 1000);

                // Timeout after 5 minutes
                setTimeout(() => {
                    clearInterval(checkClosed);
                    resolve({
                        success: false,
                        error: 'Authentication timeout'
                    });
                    cleanup();
                }, 300000);

            } catch (error) {
                console.error('🔐 AUTH: Unexpected error during OAuth flow:', error);
                resolve({
                    success: false,
                    error: `OAuth error: ${error.message}`
                });
            }
        });
    }

    /**
     * Generate random state parameter for OAuth security
     */
    private generateRandomState(): string {
        const array = new Uint8Array(16);
        crypto.getRandomValues(array);
        return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
    }

    /**
     * Build Google OAuth authorization URL
     */
    private buildOAuthUrl(state: string): string {
        const params = new URLSearchParams({
            response_type: 'code',
            client_id: this.clientId,
            redirect_uri: this.redirectUri,
            scope: this.scope,
            state: state,
            access_type: 'offline',
            prompt: 'consent'
        });

        return `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`;
    }

    /**
     * Enhanced popup authentication with better error handling
     */
    private triggerPopupAuthentication(resolve: (result: IGoogleAuthResult) => void): void {
        try {
            console.log('🔐 AUTH: Creating temporary Google Sign-In button...');

            // Create a temporary invisible container for the Google Sign-In button
            const tempContainer = document.createElement('div');
            tempContainer.id = 'google-signin-temp-container';
            tempContainer.style.cssText = `
                position: fixed;
                top: -1000px;
                left: -1000px;
                width: 1px;
                height: 1px;
                overflow: hidden;
                opacity: 0;
                pointer-events: none;
                z-index: -1;
            `;

            document.body.appendChild(tempContainer);

            // Render the Google Sign-In button
            (window as any).google.accounts.id.renderButton(tempContainer, {
                theme: 'outline',
                size: 'large',
                type: 'standard',
                shape: 'rectangular',
                text: 'signin_with',
                logo_alignment: 'left'
            });

            // Find and trigger the button
            setTimeout(() => {
                const renderedButton = tempContainer.querySelector('div[role="button"]') as HTMLElement;
                if (renderedButton) {
                    console.log('🔐 AUTH: Triggering Google Sign-In button click...');
                    renderedButton.click();
                } else {
                    console.error('🔐 AUTH: Could not find rendered Google Sign-In button');
                    this.cleanupTempContainer(tempContainer);
                    resolve({
                        success: false,
                        error: 'Failed to initialize Google Sign-In button'
                    });
                }
            }, 500);

            // Cleanup after delay
            setTimeout(() => {
                this.cleanupTempContainer(tempContainer);
            }, 10000);

        } catch (error) {
            console.error('🔐 AUTH: Error triggering popup authentication:', error);
            resolve({
                success: false,
                error: `Popup authentication error: ${error.message}`
            });
        }
    }

    /**
     * Clean up temporary container
     */
    private cleanupTempContainer(container: HTMLElement): void {
        try {
            if (document.body.contains(container)) {
                document.body.removeChild(container);
            }
        } catch (error) {
            console.warn('🔐 AUTH: Error cleaning up temp container:', error);
        }
    }

    /**
     * Enhanced Google Identity Services library loading with retry logic
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

            // Check if script is already being loaded
            const existingScript = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
            if (existingScript) {
                // Wait for existing script to load
                existingScript.addEventListener('load', () => {
                    setTimeout(() => {
                        if (typeof (window as any).google !== 'undefined' &&
                            (window as any).google.accounts &&
                            (window as any).google.accounts.id) {
                            resolve();
                        } else {
                            reject(new Error('Google Identity Services failed to initialize after script load'));
                        }
                    }, 200);
                });
                return;
            }

            // Create and load script
            const script = document.createElement('script');
            script.src = 'https://accounts.google.com/gsi/client';
            script.async = true;
            script.defer = true;

            script.onload = () => {
                // Wait for library to initialize
                setTimeout(() => {
                    if (typeof (window as any).google !== 'undefined' &&
                        (window as any).google.accounts &&
                        (window as any).google.accounts.id) {
                        resolve();
                    } else {
                        reject(new Error('Google Identity Services failed to initialize'));
                    }
                }, 200);
            };

            script.onerror = () => {
                reject(new Error('Failed to load Google Identity Services script'));
            };

            // Add to document head
            document.head.appendChild(script);
        });
    }

    /**
     * Enhanced JWT token decoding with validation
     */
    private decodeJWT(token: string): IGoogleUserInfo {
        try {
            const parts = token.split('.');
            if (parts.length !== 3) {
                throw new Error('Invalid JWT format');
            }

            const base64Url = parts[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(
                atob(base64)
                    .split('')
                    .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
                    .join('')
            );

            const decoded = JSON.parse(jsonPayload);

            // Validate required fields
            if (!decoded.email || !decoded.name || !decoded.sub) {
                throw new Error('Missing required fields in JWT token');
            }

            return decoded as IGoogleUserInfo;
        } catch (error) {
            console.error('🔐 AUTH: Error decoding JWT:', error);
            throw new Error('Failed to decode authentication token');
        }
    }

    /**
     * Validate decoded token structure and expiration
     */
    private validateDecodedToken(userInfo: IGoogleUserInfo): boolean {
        try {
            // Check required fields
            if (!userInfo.email || !userInfo.name || !userInfo.sub) {
                console.error('🔐 AUTH: Missing required fields in token');
                return false;
            }

            // Check expiration
            const now = Math.floor(Date.now() / 1000);
            if (userInfo.exp && userInfo.exp < now) {
                console.error('🔐 AUTH: Token is expired');
                return false;
            }

            // Check audience (should match our client ID)
            if (userInfo.aud !== this.clientId) {
                console.error('🔐 AUTH: Token audience does not match client ID');
                return false;
            }

            return true;
        } catch (error) {
            console.error('🔐 AUTH: Error validating token:', error);
            return false;
        }
    }

    /**
     * Check if user is currently authenticated
     */
    isAuthenticated(): boolean {
        if (!this.currentToken || !this.tokenExpirationTime) {
            return false;
        }

        // Check if token is expired
        const now = Date.now();
        if (now >= this.tokenExpirationTime) {
            console.log('🔐 AUTH: Token expired, clearing authentication');
            this.logout();
            return false;
        }

        return true;
    }

    /**
     * Get current ID token
     */
    getIdToken(): string | null {
        if (this.isAuthenticated()) {
            return this.currentToken;
        }
        return null;
    }

    /**
     * Get current user info
     */
    getUserInfo(): IGoogleUserInfo | null {
        if (this.isAuthenticated()) {
            return this.userInfo;
        }
        return null;
    }

    /**
     * Get time until token expires (in milliseconds)
     */
    getTimeUntilExpiration(): number | null {
        if (!this.tokenExpirationTime) {
            return null;
        }
        return Math.max(0, this.tokenExpirationTime - Date.now());
    }

    /**
     * Get the configured redirect URI
     */
    getRedirectUri(): string {
        return this.redirectUri;
    }

    /**
     * Enhanced logout with proper cleanup
     */
    logout(): void {
        console.log('🔐 AUTH: Logging out user');

        this.currentToken = null;
        this.userInfo = null;
        this.tokenExpirationTime = null;

        // Clear global variables
        if ((window as any).escobarGoogleIdToken) {
            delete (window as any).escobarGoogleIdToken;
        }
        if ((window as any).escobarGoogleUserInfo) {
            delete (window as any).escobarGoogleUserInfo;
        }

        // Revoke Google session if possible
        if (typeof (window as any).google !== 'undefined') {
            try {
                (window as any).google.accounts.id.disableAutoSelect();
            } catch (error) {
                console.warn('🔐 AUTH: Error disabling Google auto-select:', error);
            }
        }
    }

    /**
     * Enhanced token validation
     */
    validateToken(): boolean {
        if (!this.currentToken) {
            return false;
        }

        try {
            const decoded = this.decodeJWT(this.currentToken);
            return this.validateDecodedToken(decoded);
        } catch (error) {
            console.error('🔐 AUTH: Error validating token:', error);
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
    console.log('🔐 AUTH: Initializing Google Auth Manager');
    globalAuthManager = new GoogleAuthManager(config);
    return globalAuthManager;
}

/**
 * Get global Google Auth manager instance
 */
export function getGoogleAuthManager(): GoogleAuthManager | null {
    return globalAuthManager;
}

/**
 * Check if Google authentication is available (client ID configured)
 */
export function isGoogleAuthAvailable(): boolean {
    return globalAuthManager !== null && globalAuthManager.isAuthenticated();
}

/**
 * Update credentials by sending Google OAuth info through WebSocket to Bonnie
 */
export async function updateCredentials(
    authorizationCode: string,
    redirectUri: string,
    clientId: string,
    clientSecret?: string,
    state?: string
): Promise<{ success: boolean; error?: string; userInfo?: any }> {
    try {
        console.log('🔐 UPDATE: Sending Google OAuth credentials to Bonnie via WebSocket...');
        console.log('🔐 UPDATE: Auth code:', authorizationCode.substring(0, 20) + '...');
        console.log('🔐 UPDATE: Redirect URI:', redirectUri);
        console.log('🔐 UPDATE: Client ID:', clientId.substring(0, 20) + '...');

        // Import the WebSocket bridge to send message to Bonnie
        const { callPython } = await import('../voitta/pythonBridge_browser');

        // Get current user info from global settings
        const currentSettings = (window as any).escobarCurrentSettings;
        const username = currentSettings?.username || 'default-user';

        // Generate a unique call ID
        const call_id = `google-auth-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

        // Create a protocol message to send Google OAuth credentials to Bonnie
        // Use the proper updateCredentials method
        const googleAuthMessage = {
            method: 'updateCredentials',
            username: username,
            call_id: call_id,
            message_type: 'request' as const,
            oauth_provider: 'google' as const,
            authorization_code: authorizationCode,
            redirect_uri: redirectUri,
            client_id: clientId,
            client_secret: clientSecret,
            state: state,
            scope: 'openid email profile https://www.googleapis.com/auth/drive.readonly https://www.googleapis.com/auth/documents.readonly'
        };

        console.log('🔐 UPDATE: Sending Google OAuth message to Bonnie:', {
            method: googleAuthMessage.method,
            username: googleAuthMessage.username,
            call_id: googleAuthMessage.call_id,
            has_auth_code: !!authorizationCode,
            has_client_id: !!clientId
        });

        // Send the message through WebSocket to Bonnie
        const response = await callPython(googleAuthMessage);

        console.log('🔐 UPDATE: Received response from Bonnie:', response);

        // Check if the response indicates success
        if (response.error_type) {
            console.error('🔐 UPDATE: Bonnie returned error:', response.value);
            return {
                success: false,
                error: response.value || 'Unknown error from Bonnie'
            };
        }

        // For now, we'll extract user info from the auth code locally
        // In a full implementation, Bonnie would exchange the code for tokens and return user info
        let userInfo = null;
        try {
            // This is a placeholder - in reality, Bonnie should handle the token exchange
            // and return the user information
            userInfo = {
                email: 'user@example.com', // Placeholder
                name: 'Google User', // Placeholder
                picture: null
            };
        } catch (error) {
            console.warn('🔐 UPDATE: Could not extract user info locally:', error);
        }

        console.log('🔐 UPDATE: Google OAuth credentials sent to Bonnie successfully');

        return {
            success: true,
            userInfo: userInfo
        };

    } catch (error) {
        console.error('🔐 UPDATE: Error sending credentials to Bonnie:', error);

        return {
            success: false,
            error: `Failed to send credentials to Bonnie: ${error.message || 'Unknown error'}`
        };
    }
}
