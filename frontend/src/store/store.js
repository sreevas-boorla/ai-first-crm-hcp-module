import { configureStore } from '@reduxjs/toolkit';
import hcpReducer from './hcpSlice';
import interactionReducer from './interactionSlice';
import chatReducer from './chatSlice';

export const store = configureStore({
  reducer: {
    hcps: hcpReducer,
    interactions: interactionReducer,
    chat: chatReducer,
  },
});
