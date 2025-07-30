import { useEffect } from 'react';
export function useHandleSceneTicks(model, container) {
    useEffect(() => {
        // Plotly scenes and geo views reset when our data ticks
        // Pause rendering data updates when the user is manipulating a scene
        if (!model || !container || !model.shouldPauseOnUserInteraction()) {
            return;
        }
        function handleMouseDown() {
            model === null || model === void 0 ? void 0 : model.pauseUpdates();
            // The once option removes the listener after it is called
            window.addEventListener('mouseup', handleMouseUp, { once: true });
        }
        function handleMouseUp() {
            model === null || model === void 0 ? void 0 : model.resumeUpdates();
        }
        let wheelTimeout = 0;
        function handleWheel() {
            model === null || model === void 0 ? void 0 : model.pauseUpdates();
            window.clearTimeout(wheelTimeout);
            wheelTimeout = window.setTimeout(() => {
                model === null || model === void 0 ? void 0 : model.resumeUpdates();
            }, 300);
        }
        container.addEventListener('mousedown', handleMouseDown);
        container.addEventListener('wheel', handleWheel);
        return () => {
            window.clearTimeout(wheelTimeout);
            window.removeEventListener('mouseup', handleMouseUp);
            container.removeEventListener('mousedown', handleMouseDown);
            container.removeEventListener('wheel', handleWheel);
        };
    }, [model, container]);
}
export default useHandleSceneTicks;
//# sourceMappingURL=useHandleSceneTicks.js.map