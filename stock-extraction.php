<html>
<body>
<?php
    $mysqli = new mysqli("localhost", "root", "","stock_market");
    if ($mysqli->connect_error) {
        die("Connection failed: " . $mysqli->connect_error);
    }
    echo "Connected successfully";
    //table name
    $table="yahoo_2020_07_18_22_21_43";
    $query_str= "SELECT * FROM $table ORDER BY Price";
    $result = $mysqli->query($query_str);
    $count=$result->field_count;
    echo '<table border="1" cellspacing="2" cellpadding="2">';
    echo '<tr>';
    for($i=0;$i<$count;$i++){
        $field_info=$result->fetch_field_direct($i);
        $field_name=$field_info->name;
        echo '<td><button type="submit" name="id_sort" class="button" value="1">'. $field_name . '</button></td>';
        // echo '<td>'. $field_name . '</td>';
    }
    echo '</tr>';
    while(($row=$result->fetch_array(MYSQLI_NUM))!=NULL){
        echo '<tr>';
        for($j=0;$j<$count;$j++){
            echo '<td>'. $row[$j] . '</td>';
        }
        echo '</tr>';
    }
    echo '</table>';
    $mysqli->close();
?>
</body>
</html>