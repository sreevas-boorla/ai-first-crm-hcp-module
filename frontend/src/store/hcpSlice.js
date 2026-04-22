import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { hcpAPI } from '../services/api';

export const fetchHCPs = createAsyncThunk('hcps/fetchAll', async (search = '') => {
  const res = await hcpAPI.getAll(search);
  return res.data;
});

const hcpSlice = createSlice({
  name: 'hcps',
  initialState: {
    list: [],
    selectedHCP: null,
    loading: false,
    error: null,
  },
  reducers: {
    selectHCP: (state, action) => {
      state.selectedHCP = action.payload;
    },
    clearSelectedHCP: (state) => {
      state.selectedHCP = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchHCPs.pending, (state) => { state.loading = true; })
      .addCase(fetchHCPs.fulfilled, (state, action) => {
        state.loading = false;
        state.list = action.payload;
      })
      .addCase(fetchHCPs.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message;
      });
  },
});

export const { selectHCP, clearSelectedHCP } = hcpSlice.actions;
export default hcpSlice.reducer;
