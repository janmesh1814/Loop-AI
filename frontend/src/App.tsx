import React, { useState, useEffect } from "react";
import { Container, Grid, Typography, Box, Alert, Button } from "@mui/material";

import { SummaryCards } from "./components/SummaryCards";
import { StoreList } from "./components/StoreList";
import { OrdersTable } from "./components/OrdersTable";

import { apiService } from "./services/api";
import { Store, StoreMetrics, SummaryResponse } from "./types";

import "./App.css";

type ViewMode = "LIST" | "DETAILS";

function App() {
  const [view, setView] = useState<ViewMode>("LIST");
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [selectedStore, setSelectedStore] = useState<Store | null>(null);
  const [metrics, setMetrics] = useState<StoreMetrics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiService.getSummary().then(setSummary);
  }, []);

  const handleStoreSelect = async (store: Store) => {
    setSelectedStore(store);
    setView("DETAILS");

    setLoading(true);
    try {
      const data = await apiService.getStoreDashboard(store.id);
      setMetrics(data);
    } catch {
      setError("Failed to load store data");
    } finally {
      setLoading(false);
    }
  };

  const handleBack = () => {
    setView("LIST");
    setSelectedStore(null);
    setMetrics(null);
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ py: 3 }}>
        <Typography variant="h4" gutterBottom>
          Restaurant Dashboard
        </Typography>

        {error && <Alert severity="error">{error}</Alert>}

        {view === "LIST" && (
          <>
            {summary && <SummaryCards summary={summary} />}

            {summary?.stores && (
              <StoreList
                stores={summary.stores}
                onSelect={handleStoreSelect}
              />
            )}
          </>
        )}
        
        {view === "DETAILS" && selectedStore && (
          <>
            <Button
              variant="outlined"
              sx={{ mb: 2 }}
              onClick={handleBack}
            >
              ← Back to Stores
            </Button>

            <Typography variant="h5" gutterBottom>
              Orders for {selectedStore.name}
            </Typography>

            {loading ? (
              <Typography>Loading orders...</Typography>
            ) : (
              metrics && <OrdersTable orders={metrics.orders} />
            )}
          </>
        )}
      </Box>
    </Container>
  );
}

export default App;
