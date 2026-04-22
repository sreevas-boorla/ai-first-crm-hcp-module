import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { interactionAPI } from '../services/api';

export const fetchInteractions = createAsyncThunk('interactions/fetchAll', async (hcpId = null) => {
  const res = await interactionAPI.getAll(hcpId);
  return res.data;
});

export const createInteraction = createAsyncThunk('interactions/create', async (data) => {
  const res = await interactionAPI.create(data);
  return res.data;
});

export const updateInteraction = createAsyncThunk('interactions/update', async ({ id, data }) => {
  const res = await interactionAPI.update(id, data);
  return res.data;
});

export const deleteInteraction = createAsyncThunk('interactions/delete', async (id) => {
  await interactionAPI.delete(id);
  return id;
});

const interactionSlice = createSlice({
  name: 'interactions',
  initialState: {
    list: [],
    loading: false,
    error: null,
    successMessage: '',
  },
  reducers: {
    clearMessage: (state) => { state.successMessage = ''; state.error = null; },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => { state.loading = true; })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.list.unshift(action.payload);
        state.successMessage = 'Interaction logged successfully!';
      })
      .addCase(updateInteraction.fulfilled, (state, action) => {
        const idx = state.list.findIndex((i) => i.id === action.payload.id);
        if (idx !== -1) state.list[idx] = action.payload;
        state.successMessage = 'Interaction updated!';
      })
      .addCase(deleteInteraction.fulfilled, (state, action) => {
        state.list = state.list.filter((i) => i.id !== action.payload);
        state.successMessage = 'Interaction deleted.';
      });
  },
});

export const { clearMessage } = interactionSlice.actions;
export default interactionSlice.reducer;
