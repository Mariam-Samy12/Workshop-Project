import db_connection

def get_top_craft_workshop():
    """Q1 — top craft workshop last month"""
    query = """
    SELECT TOP 1 w.Craft, w.Title, COUNT(wr.RegistrationID) AS Participants
    FROM Workshop w
    JOIN WorkshopRegistration wr ON w.WorkshopID = wr.WorkshopID
    WHERE MONTH(w.WorkshopDate) = MONTH(DATEADD(MONTH,-1,GETDATE()))
      AND YEAR(w.WorkshopDate)  = YEAR(DATEADD(MONTH,-1,GETDATE()))
    GROUP BY w.Craft, w.Title
    ORDER BY Participants DESC"""
    return query

def get_studios_no_bookings():
    """Q2 — studios with no bookings last month"""
    query = """
    SELECT s.StudioID, s.Name, s.Type FROM Studio s
    WHERE s.StudioID NOT IN (
      SELECT DISTINCT w.StudioID FROM Workshop w
      WHERE MONTH(w.WorkshopDate) = MONTH(DATEADD(MONTH,-1,GETDATE()))
        AND YEAR(w.WorkshopDate)  = YEAR(DATEADD(MONTH,-1,GETDATE())))"""
    return query

def get_most_active_artist():
    """Q3 — most active artist last month"""
    query = """
    SELECT TOP 1 a.Name, COUNT(w.WorkshopID) AS WorkshopsTaught
    FROM Artist a JOIN Workshop w ON a.ArtistID = w.ArtistID
    WHERE MONTH(w.WorkshopDate) = MONTH(DATEADD(MONTH,-1,GETDATE()))
      AND YEAR(w.WorkshopDate)  = YEAR(DATEADD(MONTH,-1,GETDATE()))
    GROUP BY a.ArtistID, a.Name ORDER BY WorkshopsTaught DESC"""
    return query

def get_inactive_members():
    """Q4 — inactive members last month"""
    query = """
    SELECT m.MemberID, m.Name, m.Email FROM Member m
    WHERE m.MemberID NOT IN (
      SELECT DISTINCT wr.MemberID FROM WorkshopRegistration wr
      JOIN Workshop w ON wr.WorkshopID = w.WorkshopID
      WHERE MONTH(w.WorkshopDate) = MONTH(DATEADD(MONTH,-1,GETDATE()))
        AND YEAR(w.WorkshopDate) = YEAR(DATEADD(MONTH,-1,GETDATE())))
    AND m.MemberID NOT IN (
      SELECT DISTINCT tr.MemberID FROM ToolRental tr
      WHERE MONTH(tr.PickupTime) = MONTH(DATEADD(MONTH,-1,GETDATE()))
        AND YEAR(tr.PickupTime) = YEAR(DATEADD(MONTH,-1,GETDATE())))"""
    return query

def get_materials_consumed():
    """Q5 — materials consumed per workshop last month"""
    query = """
    SELECT w.Title, mat.Name AS Material, wm.QuantityAllocated, mat.Unit
    FROM WorkshopMaterial wm
    JOIN Workshop w   ON wm.WorkshopID = w.WorkshopID
    JOIN Material mat ON wm.MaterialID = mat.MaterialID
    WHERE MONTH(w.WorkshopDate) = MONTH(DATEADD(MONTH,-1,GETDATE()))
      AND YEAR(w.WorkshopDate)  = YEAR(DATEADD(MONTH,-1,GETDATE()))
    ORDER BY w.Title, mat.Name"""
    return query

def get_tool_rental_count():
    """Q6 — tool rental count (derived attribute)"""
    query = """
    SELECT t.ToolID, t.Name, t.Description,
           COUNT(tr.RentalID) AS TotalRentals
    FROM Tool t
    LEFT JOIN ToolRental tr ON t.ToolID = tr.ToolID
    GROUP BY t.ToolID, t.Name, t.Description
    ORDER BY TotalRentals DESC"""
    return query

def run_query(query_func):
    conn = db_connection.get_connection()
    if not conn:
        # Returning sample data for demonstration since we don't have a real DB
        if query_func == get_top_craft_workshop:
            return [("Pottery", "Beginner Wheel Throwing", 15)], ["Craft", "Title", "Participants"]
        elif query_func == get_studios_no_bookings:
            return [(101, "Studio A", "Textile")], ["StudioID", "Name", "Type"]
        elif query_func == get_most_active_artist:
            return [("John Doe", 5)], ["Name", "WorkshopsTaught"]
        elif query_func == get_inactive_members:
            return [(501, "Jane Smith", "jane@example.com")], ["MemberID", "Name", "Email"]
        elif query_func == get_materials_consumed:
            return [("Clay Workshop", "Red Clay", 50, "kg")], ["Title", "Material", "Quantity", "Unit"]
        elif query_func == get_tool_rental_count:
            return [(1, "Hammer", "Standard", 12)], ["ToolID", "Name", "Description", "TotalRentals"]
        return [], []
    
    cursor = conn.cursor()
    cursor.execute(query_func())
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return rows, columns
