import { Grid, Card, CardContent, Typography } from "@mui/material";
import { SummaryResponse } from "../types";

interface Props {
  summary: SummaryResponse;
}

export function SummaryCards({ summary }: Props) {
  return (
    <Grid container spacing={2} sx={{ mb: 2 }}>
      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2">Total Stores</Typography>
            <Typography variant="h5">{summary.totalStores}</Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2">Total Orders</Typography>
            <Typography variant="h5">{summary.totalOrders}</Typography>
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={4}>
        <Card>
          <CardContent>
            <Typography variant="subtitle2">Total Revenue</Typography>
            <Typography variant="h5">
              ${summary.totalRevenue.toFixed(2)}
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}
