import { AppBar, Box, IconButton, Toolbar, Typography } from '@mui/material';
import { Menu as MenuIcon } from '@mui/icons-material';

export const Layout = () => {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position='static'>
                <Toolbar>
                    <IconButton
                        size='large'
                        edge='start'
                        color='inherit'
                        sx={{ mr: 2 }}
                    >
                        <MenuIcon />
                    </IconButton>
                    <Typography variant='h6'>Receipts</Typography>
                </Toolbar>
            </AppBar>
        </Box>
    );
};

export default Layout;
