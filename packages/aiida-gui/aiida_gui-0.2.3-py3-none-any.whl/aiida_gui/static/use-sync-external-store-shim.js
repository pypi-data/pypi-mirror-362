// Pull useSyncExternalStore off the React global
const { useSyncExternalStore } = window.React;

// Export it as ESM so the plugin’s imports resolve
export default useSyncExternalStore;
export { useSyncExternalStore };
