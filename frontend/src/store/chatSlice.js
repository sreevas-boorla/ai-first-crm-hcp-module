import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { agentAPI } from '../services/api';

export const sendMessage = createAsyncThunk('chat/sendMessage', async ({ message, hcpId }) => {
  const res = await agentAPI.chat(message, hcpId);
  return res.data;
});

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [
      {
        role: 'assistant',
        content: "Hello! I'm your AI CRM assistant. I can help you log interactions with HCPs, search for doctors, review interaction history, and suggest follow-up actions. How can I help you today?",
      },
    ],
    loading: false,
    error: null,
  },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: 'user', content: action.payload });
    },
    clearChat: (state) => {
      state.messages = [
        {
          role: 'assistant',
          content: "Chat cleared. How can I help you?",
        },
      ];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => { state.loading = true; })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({ role: 'assistant', content: action.payload.reply });
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
        state.messages.push({
          role: 'assistant',
          content: '⚠ Sorry, I encountered an error. Please check that the backend is running and the Groq API key is configured.',
        });
      });
  },
});

export const { addUserMessage, clearChat } = chatSlice.actions;
export default chatSlice.reducer;
